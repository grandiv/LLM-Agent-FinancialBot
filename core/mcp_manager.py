"""
MCP (Model Context Protocol) Manager
Manages MCP server connections and tool execution for enhanced agent capabilities
"""

import os
import json
import logging
import asyncio
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
from pathlib import Path
import httpx

from .mcp_client import MCPClientManager

logger = logging.getLogger(__name__)


class MCPManager:
    """Manager for MCP server integrations"""

    def __init__(self, export_dir: str = "exports", reminders_file: str = "reminders.json"):
        """
        Initialize MCP Manager

        Args:
            export_dir: Directory for exported files
            reminders_file: JSON file to store reminders
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)

        self.reminders_file = Path(reminders_file)
        self.reminders = self._load_reminders()

        # Initialize MCP client for external servers
        self.mcp_client = MCPClientManager()

        # Initialize httpx client for LLM calls
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm_client = httpx.Client(base_url=ollama_base_url.rstrip("/"), timeout=60.0)
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

        # Cache for exchange rate (to avoid too many API calls)
        self._exchange_rate_cache = {"rate": None, "timestamp": None}

        logger.info("MCP Manager initialized")

    async def initialize_mcp(self):
        """Initialize MCP client connections"""
        try:
            success = await self.mcp_client.initialize()
            if success:
                logger.info("MCP servers connected successfully")
            else:
                logger.warning("MCP initialization failed or partially completed")
            return success
        except Exception as e:
            logger.error(f"Failed to initialize MCP: {e}", exc_info=True)
            return False

    # ============================================================================
    # FILE SYSTEM MCP SERVER
    # ============================================================================

    def export_to_csv(self, user_id: str, transactions: List[Dict],
                     balance_data: Dict) -> Dict[str, Any]:
        """
        Export financial data to CSV file

        Args:
            user_id: User ID
            transactions: List of transaction dictionaries
            balance_data: Balance summary data

        Returns:
            Dict with status, file_path, and message
        """
        try:
            # Create DataFrame from transactions
            if not transactions:
                return {
                    "success": False,
                    "message": "Tidak ada transaksi untuk diekspor"
                }

            df = pd.DataFrame(transactions)

            # Reorder columns for better readability
            column_order = ['date', 'type', 'amount', 'category', 'description']
            df = df[[col for col in column_order if col in df.columns]]

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_report_{user_id}_{timestamp}.csv"
            filepath = self.export_dir / filename

            # Export to CSV with explicit file handling
            with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
                df.to_csv(f, index=False)

            # Verify file was created successfully
            if not filepath.exists():
                raise FileNotFoundError(f"CSV file was not created: {filepath}")

            logger.info(f"Exported CSV for user {user_id}: {filepath} (size: {filepath.stat().st_size} bytes)")

            return {
                "success": True,
                "file_path": str(filepath),
                "filename": filename,
                "row_count": len(df),
                "message": f"✅ Berhasil mengekspor {len(df)} transaksi ke {filename}"
            }

        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal mengekspor ke CSV: {str(e)}"
            }

    def export_to_excel(self, user_id: str, transactions: List[Dict],
                       balance_data: Dict, category_report: Dict) -> Dict[str, Any]:
        """
        Export financial data to Excel file with multiple sheets

        Args:
            user_id: User ID
            transactions: List of transaction dictionaries
            balance_data: Balance summary data
            category_report: Category breakdown data

        Returns:
            Dict with status, file_path, and message
        """
        try:
            if not transactions:
                return {
                    "success": False,
                    "message": "Tidak ada transaksi untuk diekspor"
                }

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"financial_report_{user_id}_{timestamp}.xlsx"
            filepath = self.export_dir / filename

            # Create Excel writer with explicit engine and mode
            writer = pd.ExcelWriter(filepath, engine='openpyxl', mode='w')

            try:
                # Sheet 1: Transactions
                df_trans = pd.DataFrame(transactions)
                column_order = ['date', 'type', 'amount', 'category', 'description']
                df_trans = df_trans[[col for col in column_order if col in df_trans.columns]]
                df_trans.to_excel(writer, sheet_name='Transactions', index=False)

                # Sheet 2: Summary
                summary_data = {
                    'Metric': ['Total Pemasukan', 'Total Pengeluaran', 'Saldo'],
                    'Amount': [
                        balance_data['income'],
                        balance_data['expense'],
                        balance_data['balance']
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='Summary', index=False)

                # Sheet 3: Category Breakdown
                if category_report:
                    category_data = []
                    for category, amounts in category_report.items():
                        if amounts['income'] > 0:
                            category_data.append({
                                'Category': category,
                                'Type': 'Income',
                                'Amount': amounts['income']
                            })
                        if amounts['expense'] > 0:
                            category_data.append({
                                'Category': category,
                                'Type': 'Expense',
                                'Amount': amounts['expense']
                            })

                    if category_data:
                        df_category = pd.DataFrame(category_data)
                        df_category.to_excel(writer, sheet_name='Categories', index=False)

            finally:
                # Explicitly save and close the writer
                writer.close()

            # Verify file was created successfully
            if not filepath.exists():
                raise FileNotFoundError(f"Excel file was not created: {filepath}")

            logger.info(f"Exported Excel for user {user_id}: {filepath} (size: {filepath.stat().st_size} bytes)")

            return {
                "success": True,
                "file_path": str(filepath),
                "filename": filename,
                "row_count": len(transactions),
                "message": f"✅ Berhasil mengekspor laporan lengkap ke {filename}\n" +
                          f"📊 File berisi {len(transactions)} transaksi dengan 3 sheet:\n" +
                          "  • Transactions (detail transaksi)\n" +
                          "  • Summary (ringkasan keuangan)\n" +
                          "  • Categories (breakdown per kategori)"
            }

        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal mengekspor ke Excel: {str(e)}"
            }

    # ============================================================================
    # URL CLEANING UTILITIES
    # ============================================================================

    def _clean_redirect_url(self, url: str) -> str:
        """
        Extract actual URL from Bing redirect URLs

        Examples:
        - Bing: https://www.bing.com/ck/a?...&u=a1aHR0cHM6Ly9zaXRlLmNvbQ&... -> https://site.com (base64 decoded)
        - Direct: https://site.com -> https://site.com (unchanged)

        Args:
            url: URL that might be a redirect

        Returns:
            Cleaned actual URL
        """
        from urllib.parse import urlparse, parse_qs, unquote
        import base64

        try:
            # Bing redirect: https://www.bing.com/ck/a?...&u=base64_encoded_url
            if 'bing.com/ck/a' in url or 'bing.com/aclick' in url:
                parsed = urlparse(url)
                params = parse_qs(parsed.query)
                if 'u' in params:
                    # Bing encodes URL with a version prefix (e.g., "a1")
                    encoded = params['u'][0]
                    try:
                        # Strip version prefix (first 2 chars) if present
                        if len(encoded) > 2 and encoded[0] == 'a' and encoded[1].isdigit():
                            encoded = encoded[2:]

                        # Decode base64
                        decoded = base64.b64decode(encoded + '==').decode('utf-8')

                        # Extract URL from decoded string
                        if decoded.startswith('http'):
                            return decoded.split()[0]  # Take first URL-like token
                    except Exception as decode_error:
                        logger.debug(f"Failed to decode Bing URL: {decode_error}")
                        # Try URL unquote as alternative
                        try:
                            unquoted = unquote(encoded)
                            if unquoted.startswith('http'):
                                return unquoted
                        except:
                            pass

            # Already a direct URL
            return url

        except Exception as e:
            logger.debug(f"Error cleaning URL {url}: {e}")
            return url

    def _generate_price_message(self, item_name: str, prices_list: List[Dict], min_price: int, max_price: int, avg_price: int) -> str:
        """
        Generate natural Indonesian message based on deduplicated price results

        Args:
            item_name: Item being searched
            prices_list: List of deduplicated price info dicts
            min_price: Minimum price (may not be meaningful if mixed currencies)
            max_price: Maximum price (may not be meaningful if mixed currencies)
            avg_price: Average price (may not be meaningful if mixed currencies)

        Returns:
            Natural Indonesian message
        """
        try:
            # Group prices by currency
            grouped_by_currency = {}
            for p in prices_list:
                currency = p.get('currency', 'IDR')
                if currency not in grouped_by_currency:
                    grouped_by_currency[currency] = []
                grouped_by_currency[currency].append(p)

            # Create prompt for message generation
            sources_text = ""
            for currency, items in grouped_by_currency.items():
                currency_symbol = "$" if currency == "USD" else "Rp" if currency == "IDR" else currency
                sources_text += f"\n{currency} Prices:\n"
                for p in items:
                    price = p.get('price', 0)
                    title = p.get('title', 'Unknown')
                    url = p.get('url', 'unknown')
                    sources_text += f"- {title} ({currency_symbol} {price:,}) dari {url}\n"

            prompt = f"""Generate a natural, conversational message in Indonesian to inform the user about price search results.

ITEM SEARCHED: "{item_name}"

NUMBER OF SOURCES: {len(prices_list)} unique websites

PRICES FOUND (BY CURRENCY):
{sources_text}

Generate a natural, friendly message in Indonesian (2-3 sentences) that:
1. Mentions prices found with their ORIGINAL currencies (Rp for Indonesia, $ for USA, etc.)
2. States the number of unique sources/websites
3. If both Indonesian and international prices are found, mention both clearly
4. Provides helpful context or advice

**IMPORTANT:** State each price with its currency symbol explicitly (Rp or $). DO NOT convert.

Be conversational and helpful. Don't use bullet points or structured format.

Return ONLY the message text in Indonesian, nothing else."""

            # Call LLM
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": "You are a helpful Indonesian shopping assistant. Generate natural, conversational messages."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,  # Slightly higher for more natural language
                    "num_predict": 300,
                }
            }

            resp = self.llm_client.post("/api/chat", json=payload)
            resp.raise_for_status()
            response_data = resp.json()

            message_text = response_data.get("message", {}).get("content", "")

            # Handle thinking tags
            if "<think>" in message_text and "</think>" in message_text:
                message_text = message_text.split("</think>")[-1].strip()

            return message_text.strip()

        except Exception as e:
            logger.error(f"Error generating price message: {e}")
            # Fallback to simple message - group by currency
            grouped = {}
            for p in prices_list:
                currency = p.get('currency', 'IDR')
                if currency not in grouped:
                    grouped[currency] = []
                grouped[currency].append(p.get('price', 0))

            price_summary = []
            for currency, prices in grouped.items():
                symbol = "$" if currency == "USD" else "Rp" if currency == "IDR" else currency
                min_p = min(prices)
                max_p = max(prices)
                price_summary.append(f"{symbol} {min_p:,} - {symbol} {max_p:,}")

            return f"Saya menemukan {len(prices_list)} sumber harga untuk '{item_name}': {', '.join(price_summary)}."

    def _extract_urls_from_search_results(self, search_text: str) -> List[Dict[str, str]]:
        """
        Extract URLs and titles from web search results

        Args:
            search_text: Raw search result text from MCP

        Returns:
            List of dicts with 'title' and 'url' keys
        """
        try:
            import re
            from urllib.parse import urlparse

            urls = []
            seen_domains = set()

            # Pattern to match URLs in search results
            # Search results typically have format: "Title - URL" or "Title\nURL"
            url_pattern = r'https?://[^\s\n<>"\'\)]+[^\s\n<>"\'\)\.,;:]'

            # Find all URLs
            found_urls = re.findall(url_pattern, search_text)

            for url in found_urls:
                try:
                    # Clean the URL
                    cleaned_url = self._clean_redirect_url(url)

                    # Parse domain
                    parsed = urlparse(cleaned_url)
                    domain = parsed.netloc.lower()

                    # Remove www. prefix
                    if domain.startswith("www."):
                        domain = domain[4:]

                    # Skip if we've seen this domain
                    if domain in seen_domains:
                        continue

                    # Skip common non-content domains
                    skip_domains = ['google.com', 'bing.com', 'duckduckgo.com', 'brave.com']
                    if any(skip in domain for skip in skip_domains):
                        continue

                    # Try to extract title (look for text before the URL)
                    title = domain  # Default to domain

                    # Search for title in the text near the URL
                    url_index = search_text.find(url)
                    if url_index > 0:
                        # Look backwards for title (up to 200 chars)
                        start_index = max(0, url_index - 200)
                        before_text = search_text[start_index:url_index]

                        # Try to find a title-like pattern (text before newline or dash)
                        title_match = re.search(r'([^\n]{10,150}?)[\n\-–—]', before_text[::-1])
                        if title_match:
                            title = title_match.group(1)[::-1].strip()

                    urls.append({
                        'url': cleaned_url,
                        'title': title if title != domain else f"Source from {domain}",
                        'domain': domain
                    })

                    seen_domains.add(domain)

                    # Limit to 10 unique sources
                    if len(urls) >= 10:
                        break

                except Exception as e:
                    logger.debug(f"Failed to parse URL {url}: {e}")
                    continue

            logger.info(f"Extracted {len(urls)} unique source URLs from search results")
            return urls

        except Exception as e:
            logger.error(f"Error extracting URLs from search results: {e}")
            return []

    def _preprocess_search_results(self, text_content: str) -> str:
        """
        Pre-process search results to clean redirect URLs before passing to LLM

        This ensures the LLM sees actual website URLs instead of Bing redirect URLs,
        making it easier to identify unique sources.

        Args:
            text_content: Raw search result text with Bing redirect URLs

        Returns:
            Processed text with cleaned URLs
        """
        try:
            # Find all URLs in the format "URL: https://..."
            url_pattern = r'(URL:\s*)(https?://[^\s]+)'

            def replace_url(match):
                prefix = match.group(1)  # "URL: "
                raw_url = match.group(2)  # The URL itself
                cleaned_url = self._clean_redirect_url(raw_url)

                # Log cleaning for debugging
                if cleaned_url != raw_url:
                    logger.debug(f"Cleaned URL: {raw_url[:80]}... -> {cleaned_url}")

                return f"{prefix}{cleaned_url}"

            # Replace all URLs in the text
            processed_text = re.sub(url_pattern, replace_url, text_content)

            logger.info(f"Pre-processed search results: cleaned {len(re.findall(url_pattern, text_content))} URLs")

            return processed_text

        except Exception as e:
            logger.error(f"Error pre-processing search results: {e}")
            return text_content  # Return original on error

    def _extract_prices_with_llm(self, search_result_text: str, item_name: str) -> Dict[str, Any]:
        """
        Use LLM to intelligently extract prices from search results

        The LLM can understand context and distinguish between:
        - Real product prices vs promotional text
        - Bundles vs individual items
        - Different product variants
        - Currency formatting variations

        Args:
            search_result_text: Raw search result text from MCP
            item_name: Item being searched

        Returns:
            Dict with extracted price information
        """
        try:
            logger.info(f"Using LLM to extract prices from search results for: {item_name}")

            # Pre-process search results to clean redirect URLs
            cleaned_text = self._preprocess_search_results(search_result_text)

            # Create specialized prompt for price extraction
            price_extraction_prompt = f"""You are a price extraction assistant. Analyze the following web search results and extract accurate product prices in THEIR ORIGINAL CURRENCY.

SEARCH QUERY: "{item_name}"

SEARCH RESULTS:
{cleaned_text[:15000]}

INSTRUCTIONS:
1. Identify REAL product prices (ignore promotional text, discounts descriptions, or fake numbers)
2. Extract prices in ORIGINAL currency (Rp for Indonesia, USD for USA, etc.)
3. **CRITICAL: Include currency field** - "IDR" for Rupiah, "USD" for US Dollars
4. **CRITICAL: Handle decimal prices correctly**:
   - For USD: "$249.99" → extract as 249 (round to nearest dollar)
   - For USD: "$1,999.00" → extract as 1999 (remove cents)
   - For IDR: "Rp 3.999.000" or "Rp 3,999,000" → extract as 3999000 (no decimals)
   - **NEVER** extract "$249.99" as 24999 - that's wrong!
5. Match each price with its source title and EXACT URL from the search results
6. **IMPORTANT: Return UNIQUE sources only** - If the same website/domain appears multiple times with different prices, pick the LOWEST price for that source
7. Group by website domain (e.g., tokopedia.com, shopee.co.id, amazon.com)
8. Distinguish between different product variants from DIFFERENT sellers
9. Return up to 5 UNIQUE sources with the best prices

Return ONLY a JSON object in this exact format (no additional text):
{{
  "success": true,
  "prices": [
    {{"price": 25000000, "currency": "IDR", "title": "iPhone 16 Pro 256GB dari Tokopedia", "url": "https://www.tokopedia.com/apple/iphone-16-pro-256gb-natural-titanium"}},
    {{"price": 1999, "currency": "USD", "title": "iPhone 16 Pro from Amazon USA", "url": "https://www.amazon.com/dp/B0DGHP6JXL"}},
    {{"price": 249, "currency": "USD", "title": "AirPods Pro from Best Buy", "url": "https://www.bestbuy.com/site/apple-airpods-pro/12345"}}
  ]
}}

PRICE EXTRACTION EXAMPLES:
- If you see "$249.99" → extract as {{"price": 249, "currency": "USD"}}  ✅ CORRECT
- If you see "$1,999.00" → extract as {{"price": 1999, "currency": "USD"}}  ✅ CORRECT
- If you see "Rp 3.999.000" → extract as {{"price": 3999000, "currency": "IDR"}}  ✅ CORRECT
- NEVER do "$249.99" → {{"price": 24999, "currency": "USD"}}  ❌ WRONG!

If no valid prices found, return:
{{
  "success": false,
  "reason": "Brief reason why no prices found"
}}

CRITICAL RULES:
- NO duplicate domains (tokopedia.com should appear ONCE, not 5 times)
- Each entry must be from a DIFFERENT website
- **NEVER make up or generate URLs** - ONLY use URLs that EXACTLY appear in the search results above
- If you cannot find the exact URL for a price, use empty string "" for the url field
- ALWAYS include "currency" field ("IDR", "USD", "SGD", etc.)
- Store price as numeric value WITHOUT currency symbols
- Return ONLY the JSON object, nothing else.

**IMPORTANT:** If you cannot find the EXACT full URL in the search results, DO NOT generate or create a URL. Use "" instead."""

            # Call Ollama API
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": "You are a price extraction expert. Always return valid JSON. IMPORTANT: Extract decimal prices correctly - $249.99 is 249 USD, not 24999!"},
                    {"role": "user", "content": price_extraction_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Lower temperature for more consistent extraction
                    "num_predict": 1500,
                }
            }

            logger.info(f"Calling LLM ({self.ollama_model}) for price extraction...")
            resp = self.llm_client.post("/api/chat", json=payload)
            resp.raise_for_status()
            response_data = resp.json()

            # Extract response text
            response_text = response_data.get("message", {}).get("content", "")

            # Handle thinking tags if present
            if "<think>" in response_text and "</think>" in response_text:
                response_text = response_text.split("</think>")[-1].strip()

            # Parse JSON response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                llm_result = json.loads(json_str)

                logger.info(f"LLM extraction result: {llm_result.get('reasoning', 'No reasoning')}")

                if llm_result.get("success") and llm_result.get("prices"):
                    prices_list = llm_result["prices"]

                    # Post-process to ensure unique sources (deduplicate by domain)
                    from urllib.parse import urlparse
                    unique_sources = {}

                    for price_info in prices_list:
                        url = price_info.get("url", "")
                        price = price_info.get("price", 0)

                        if not url or not price:
                            continue

                        # Validate URL actually appears in search results (anti-hallucination check)
                        if url not in cleaned_text:
                            logger.warning(f"LLM hallucinated URL (not found in search results): {url}")
                            # Try to find a similar URL from the search results
                            try:
                                parsed = urlparse(url)
                                domain = parsed.netloc.lower()
                                if domain.startswith("www."):
                                    domain = domain[4:]

                                # Search for any URL from this domain in the actual results
                                import re
                                url_pattern = rf'https?://(?:www\.)?{re.escape(domain)}[^\s\n<>"\'\)]*'
                                found_urls = re.findall(url_pattern, cleaned_text)

                                if found_urls:
                                    # Use the first real URL from this domain
                                    url = found_urls[0]
                                    price_info["url"] = url
                                    logger.info(f"Replaced hallucinated URL with real URL from same domain: {url}")
                                else:
                                    logger.warning(f"No real URLs found for domain {domain}, marking URL as suspicious")
                                    # Keep the URL but mark it with a warning flag
                                    price_info["url_verified"] = False
                            except Exception as e:
                                logger.error(f"Error validating URL: {e}")

                        # Extract domain from URL
                        try:
                            parsed = urlparse(url)
                            domain = parsed.netloc.lower()

                            # Remove www. prefix for better matching
                            if domain.startswith("www."):
                                domain = domain[4:]

                            # Keep lowest price for each domain
                            if domain not in unique_sources or price < unique_sources[domain]["price"]:
                                unique_sources[domain] = price_info
                                currency = price_info.get("currency", "IDR")
                                currency_symbol = "$" if currency == "USD" else "Rp"
                                logger.debug(f"Added/Updated source: {domain} - {currency_symbol} {price:,}")
                            else:
                                currency = price_info.get("currency", "IDR")
                                currency_symbol = "$" if currency == "USD" else "Rp"
                                logger.debug(f"Skipped duplicate domain: {domain} - {currency_symbol} {price:,}")

                        except Exception as e:
                            logger.warning(f"Failed to parse URL {url}: {e}")
                            # If URL parsing fails, use as-is
                            unique_sources[url] = price_info

                    # Convert back to list
                    prices_list = list(unique_sources.values())

                    logger.info(f"After deduplication: {len(prices_list)} unique sources from {len(llm_result.get('prices', []))} total")

                    if prices_list:
                        # Separate prices by currency (CRITICAL: cannot mix IDR and USD!)
                        prices_by_currency = {}
                        for p in prices_list:
                            currency = p.get("currency", "IDR")
                            if currency not in prices_by_currency:
                                prices_by_currency[currency] = []
                            prices_by_currency[currency].append(p.get("price", 0))

                        # Calculate min/max/avg per currency
                        price_ranges = {}
                        for currency, price_values in prices_by_currency.items():
                            if price_values:
                                price_ranges[currency] = {
                                    "min": min(price_values),
                                    "max": max(price_values),
                                    "avg": sum(price_values) // len(price_values)
                                }
                                logger.info(f"{currency} price range: {price_ranges[currency]}")

                        # For backward compatibility, use IDR if available, otherwise use first currency
                        if "IDR" in price_ranges:
                            min_price = price_ranges["IDR"]["min"]
                            max_price = price_ranges["IDR"]["max"]
                            avg_price = price_ranges["IDR"]["avg"]
                        else:
                            first_currency = list(price_ranges.keys())[0]
                            min_price = price_ranges[first_currency]["min"]
                            max_price = price_ranges[first_currency]["max"]
                            avg_price = price_ranges[first_currency]["avg"]

                        # Generate natural message AFTER deduplication for consistency
                        logger.info(f"Generating natural message for {len(prices_list)} unique sources")
                        natural_message = self._generate_price_message(
                            item_name=item_name,
                            prices_list=prices_list,
                            min_price=min_price,
                            max_price=max_price,
                            avg_price=avg_price
                        )

                        # Build final message with natural text + source links
                        message = f"{natural_message}\n\n"

                        # Add clickable source links
                        if len(prices_list) > 0:
                            message += "🔗 **Sumber:**\n"
                            for i, price_info in enumerate(prices_list[:5], 1):
                                price = price_info.get("price", 0)
                                currency = price_info.get("currency", "IDR")
                                title = price_info.get("title", "Unknown")[:70]
                                url = price_info.get("url", "")

                                # Format price with correct currency symbol
                                if currency == "USD":
                                    price_str = f"${price:,.0f}"
                                elif currency == "IDR":
                                    price_str = f"Rp {price:,.0f}"
                                else:
                                    price_str = f"{currency} {price:,.0f}"

                                message += f"{i}. {price_str} - {title}\n"
                                if url:
                                    message += f"   {url}\n"

                        return {
                            "success": True,
                            "item": item_name,
                            "price_range": {
                                "min": min_price,
                                "max": max_price,
                                "avg": avg_price
                            },
                            "source": "Web Search MCP + LLM",
                            "sample_count": len(prices_list),
                            "sources": [(p.get("price", 0), p.get("url", ""), p.get("title", "")) for p in prices_list[:5]],
                            "message": message
                        }

                # LLM found no prices
                reason = llm_result.get("reason", "Tidak menemukan harga yang valid")
                no_price_message = f"Maaf, saya tidak menemukan harga untuk '{item_name}'.\n\n"
                no_price_message += f"Alasan: {reason}\n\n"
                no_price_message += "💡 Coba sebutkan item dengan lebih detail atau spesifik (contoh: 'iPhone 15 Pro', 'Laptop ASUS ROG')."

                return {
                    "success": False,
                    "item": item_name,
                    "message": no_price_message
                }
            else:
                logger.warning("No JSON found in LLM response")
                return {"success": False, "item": item_name}

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            logger.debug(f"LLM response text: {response_text[:500]}")
            return {"success": False, "item": item_name}
        except Exception as e:
            logger.error(f"Error in LLM price extraction: {e}", exc_info=True)
            return {"success": False, "item": item_name}

    def _get_usd_to_idr_rate(self) -> float:
        """
        Get real-time USD to IDR exchange rate
        Uses cache to avoid excessive API calls (refreshes every 30 minutes)

        Returns:
            Exchange rate as float (e.g., 15700.0 means $1 = Rp 15,700)
        """
        try:
            from datetime import datetime, timedelta

            # Check cache (30 minutes validity)
            if self._exchange_rate_cache["rate"] and self._exchange_rate_cache["timestamp"]:
                age = datetime.now() - self._exchange_rate_cache["timestamp"]
                if age < timedelta(minutes=30):
                    logger.debug(f"Using cached exchange rate: {self._exchange_rate_cache['rate']}")
                    return self._exchange_rate_cache["rate"]

            # Fetch new rate from free API (no key required)
            logger.info("Fetching real-time USD to IDR exchange rate...")

            # Try exchangerate-api.com (free, no key required)
            with httpx.Client(timeout=10.0) as client:
                response = client.get("https://api.exchangerate-api.com/v4/latest/USD")
                response.raise_for_status()
                data = response.json()

                # Extract IDR rate
                if "rates" in data and "IDR" in data["rates"]:
                    rate = float(data["rates"]["IDR"])
                    logger.info(f"Fetched exchange rate: $1 = Rp {rate:,.0f}")

                    # Update cache
                    self._exchange_rate_cache["rate"] = rate
                    self._exchange_rate_cache["timestamp"] = datetime.now()

                    return rate
                else:
                    raise ValueError("IDR rate not found in API response")

        except Exception as e:
            logger.warning(f"Failed to fetch exchange rate: {e}")
            # Fallback to approximate rate
            fallback_rate = 15700.0
            logger.info(f"Using fallback rate: $1 = Rp {fallback_rate:,.0f}")
            return fallback_rate

    def _convert_dollars_to_rupiah(self, text: str, exchange_rate: float) -> str:
        """
        Pre-process text to convert all dollar amounts to Rupiah
        Finds patterns like $799, $1,299.99, USD 1000, etc. and adds Rupiah equivalent

        Args:
            text: Text containing dollar amounts
            exchange_rate: Current USD to IDR rate

        Returns:
            Text with Rupiah conversions added
        """
        try:
            # Regex patterns for dollar amounts (order matters - more specific first)
            # Pattern explanation: matches numbers like 799, 1199, 1,299, 10000, 10,000.99
            patterns = [
                (r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)', 'dollar_sign'),  # $799, $1,299.99, $1199
                (r'USD\s+(\d+(?:,\d{3})*(?:\.\d{2})?)', 'usd_prefix'),  # USD 799, USD 1199, USD 1,199
                (r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s+USD', 'usd_suffix'),  # 799 USD, 1599 USD, 1,599 USD
            ]

            converted_text = text

            for pattern, pattern_type in patterns:
                matches = re.finditer(pattern, converted_text, re.IGNORECASE)

                # Process matches in reverse to avoid offset issues
                for match in reversed(list(matches)):
                    # Extract the numeric value
                    amount_str = match.group(1).replace(',', '')
                    try:
                        amount = float(amount_str)

                        # Convert to Rupiah
                        rupiah = amount * exchange_rate

                        # Format the conversion annotation
                        if pattern_type == 'dollar_sign':
                            # $799 → $799 (Rp 13,282,000)
                            original = match.group(0)
                            replacement = f"{original} (Rp {rupiah:,.0f})"
                        elif pattern_type == 'usd_suffix':
                            # 799 USD → 799 USD (Rp 13,282,000)
                            original = match.group(0)
                            replacement = f"{original} (Rp {rupiah:,.0f})"
                        elif pattern_type == 'usd_prefix':
                            # USD 799 → USD 799 (Rp 13,282,000)
                            original = match.group(0)
                            replacement = f"{original} (Rp {rupiah:,.0f})"

                        # Replace in text
                        start, end = match.span()
                        converted_text = converted_text[:start] + replacement + converted_text[end:]

                    except (ValueError, TypeError) as e:
                        logger.debug(f"Could not convert amount '{amount_str}': {e}")
                        continue

            logger.info(f"Pre-processed text: converted {len(list(re.finditer(r'\(Rp [0-9,]+\)', converted_text)))} dollar amounts")
            return converted_text

        except Exception as e:
            logger.error(f"Error in dollar conversion: {e}", exc_info=True)
            return text  # Return original text if conversion fails

    def _summarize_search_results(self, search_text: str, search_query: str) -> str:
        """
        Use LLM to summarize web search results into a helpful response

        Args:
            search_text: Raw search results from MCP
            search_query: Original search query

        Returns:
            Natural Indonesian summary
        """
        try:
            logger.info(f"Summarizing search results for: {search_query}")

            # Create prompt for summarization
            summary_prompt = f"""You are a helpful assistant. Summarize the following web search results in Indonesian.

SEARCH QUERY: "{search_query}"

WEB SEARCH RESULTS:
{search_text[:10000]}

**IMPORTANT - CURRENCY REPORTING:**
State prices EXPLICITLY with their original currency:
- Indonesian prices: Use "Rp" (e.g., "Rp 25,000,000")
- US/International prices: Use "$" or "USD" (e.g., "$1,999" or "USD 1999")

DO NOT convert currencies automatically. Let the user see the original prices.

INSTRUCTIONS:
1. Provide a clear, concise summary in Indonesian (3-5 paragraphs max)
2. Focus on the most relevant and recent information
3. **State each price with its currency clearly** (Rp for Indonesia, $ for USA, etc.)
4. If multiple countries/sources are found, group them by location
5. Be conversational and helpful
7. Include specific details, specs, or features if relevant
8. If results are about products, mention key differentiators

Return ONLY the summary text in Indonesian, nothing else."""

            # Call Ollama API
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": "You are a helpful Indonesian assistant that summarizes web search results."},
                    {"role": "user", "content": summary_prompt}
                ],
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 800,
                }
            }

            resp = self.llm_client.post("/api/chat", json=payload)
            resp.raise_for_status()
            response_data = resp.json()

            summary_text = response_data.get("message", {}).get("content", "")

            # Handle thinking tags
            if "<think>" in summary_text and "</think>" in summary_text:
                summary_text = summary_text.split("</think>")[-1].strip()

            return summary_text.strip() if summary_text else "Informasi ditemukan tapi gagal diproses. Coba lagi ya!"

        except Exception as e:
            logger.error(f"Error summarizing search results: {e}")
            # Fallback: return first 1000 chars
            return f"Hasil pencarian untuk '{search_query}':\n\n{search_text[:1000]}..."

    # ============================================================================
    # WEB SEARCH MCP SERVER (Bing -> Brave -> DuckDuckGo)
    # ============================================================================

    async def web_search(self, search_query: str) -> Dict[str, Any]:
        """
        General-purpose web search for ANY information (not just prices)

        Use this for:
        - Product information and specs
        - Reviews and comparisons
        - News and updates
        - General knowledge
        - Any question that needs internet data

        Args:
            search_query: Search query in any language

        Returns:
            Dict with search results formatted for user
        """
        try:
            logger.info(f"Web search: {search_query}")

            # Use MCP web search if available
            if self.mcp_client.enabled and self.mcp_client.is_connected("web-search"):
                try:
                    logger.info("Using Web Search MCP for general search")

                    # Call MCP web search tool
                    result = await asyncio.wait_for(
                        self.mcp_client.web_search(
                            query=search_query,
                            limit=10,
                            include_content=True
                        ),
                        timeout=20.0
                    )

                    # Extract text from result
                    search_text = ""
                    if hasattr(result, 'content'):
                        content = result.content
                        if isinstance(content, list) and len(content) > 0:
                            if hasattr(content[0], 'text'):
                                search_text = content[0].text
                            else:
                                search_text = str(content[0])
                        else:
                            search_text = str(content)
                    else:
                        search_text = str(result)

                    # Extract URLs from search results
                    source_urls = self._extract_urls_from_search_results(search_text)

                    if search_text and len(search_text) > 50:
                        # Let LLM summarize the search results
                        summary = self._summarize_search_results(search_text, search_query)

                        # Build message with sources
                        message = f"🔍 **Hasil pencarian untuk '{search_query}':**\n\n{summary}"

                        # Add source links if available
                        if source_urls:
                            message += "\n\n🔗 **Sumber:**\n"
                            for i, url_info in enumerate(source_urls[:5], 1):
                                title = url_info.get('title', 'Unknown')[:80]
                                url = url_info.get('url', '')
                                message += f"{i}. {title}\n"
                                if url:
                                    message += f"   {url}\n"
                        else:
                            message += "\n\n📊 Sumber: Web Search MCP (Bing/Brave/DuckDuckGo)"

                        return {
                            "success": True,
                            "query": search_query,
                            "message": message
                        }
                    else:
                        logger.warning("Web search returned empty or very short results")
                        return {
                            "success": False,
                            "query": search_query,
                            "message": f"🔍 Pencarian untuk '{search_query}' tidak menemukan hasil yang cukup. Coba kata kunci yang lebih spesifik."
                        }

                except asyncio.TimeoutError:
                    logger.warning("Web search timed out")
                    return {
                        "success": False,
                        "query": search_query,
                        "message": "Pencarian memakan waktu terlalu lama. Coba lagi dengan query yang lebih spesifik."
                    }
                except Exception as e:
                    logger.error(f"MCP web search error: {e}", exc_info=True)
                    return {
                        "success": False,
                        "query": search_query,
                        "message": f"Maaf, terjadi error saat mencari informasi. Coba lagi ya!"
                    }
            else:
                logger.warning("Web search MCP not available")
                return {
                    "success": False,
                    "query": search_query,
                    "message": "Web search tidak tersedia saat ini. Pastikan MCP web search sudah dikonfigurasi."
                }

        except Exception as e:
            logger.error(f"Error in web_search: {e}", exc_info=True)
            return {
                "success": False,
                "query": search_query,
                "message": f"Terjadi kesalahan: {str(e)}"
            }

    async def search_price(self, item_name: str) -> Dict[str, Any]:
        """
        Search for current price of an item online using Web Search MCP

        Search priority:
        1. Web Search MCP: Bing -> Brave -> DuckDuckGo (browser automation)
        2. Database fallback (estimates)

        No API keys required! All searches are free and unlimited.

        Args:
            item_name: Name of the item to search

        Returns:
            Dict with price range and source information
        """
        try:
            logger.info(f"Searching price for: {item_name}")

            # Simple search query - let search engine find the best results
            search_query = f"{item_name} price"
            logger.info(f"Search query: {search_query}")

            # Try Web Search MCP (with timeout to prevent hanging)
            if self.mcp_client.enabled and self.mcp_client.is_connected("web-search"):
                logger.info("Using Web Search MCP (Bing -> Brave -> DuckDuckGo)")
                try:
                    # Use full-web-search for better content extraction with 20s timeout
                    result = await asyncio.wait_for(
                        self.mcp_client.web_search(
                            query=search_query,
                            limit=10,
                            include_content=True  # Changed from False - use full content extraction
                        ),
                        timeout=20.0
                    )

                    # Log the raw MCP result for debugging
                    logger.info(f"MCP search returned: type={type(result)}")
                    if hasattr(result, '__dict__'):
                        logger.info(f"MCP result attributes: {result.__dict__.keys()}")
                        logger.debug(f"Full MCP result: {result.__dict__}")

                    # Parse search results to extract prices
                    price_info = self._extract_prices_from_web_search(result, item_name)

                    if price_info["success"]:
                        return price_info
                    else:
                        logger.warning("No prices found in MCP results, using fallback")

                except asyncio.TimeoutError:
                    logger.warning(f"Web Search MCP timed out after 20 seconds, using fallback")
                    # Fall through to database fallback
                except Exception as e:
                    logger.warning(f"Web Search MCP error: {e}")
                    # Fall through to database fallback

            # Final fallback to database
            logger.info("Web Search MCP unavailable, using database fallback")
            return await self._search_price_fallback(item_name)

        except Exception as e:
            logger.error(f"Error searching price: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal mencari harga: {str(e)}"
            }

    def _extract_prices_from_web_search(self, search_result: Any, item_name: str) -> Dict[str, Any]:
        """
        Extract price information from Web Search MCP results using LLM

        Instead of regex patterns, this uses the LLM to intelligently understand
        context and extract real prices while ignoring promotional text, bundles,
        and other noise.

        Args:
            search_result: Raw search result from Web Search MCP
            item_name: Item being searched

        Returns:
            Dict with extracted price information and source URLs
        """
        try:
            # Parse MCP result to get full text content
            text_content = ""
            if hasattr(search_result, 'content'):
                content = search_result.content
                if isinstance(content, list) and len(content) > 0:
                    if hasattr(content[0], 'text'):
                        text_content = content[0].text
                    else:
                        text_content = str(content[0])
                else:
                    text_content = str(content)
            else:
                text_content = str(search_result)

            logger.info(f"Extracting prices using LLM from search results (length: {len(text_content)} chars)")

            # Use LLM for intelligent price extraction
            result = self._extract_prices_with_llm(text_content, item_name)

            if result.get("success"):
                logger.info(f"LLM successfully extracted {result.get('sample_count', 0)} prices")
            else:
                logger.warning(f"LLM could not extract prices: {result.get('message', 'Unknown reason')}")

            return result

        except Exception as e:
            logger.error(f"Error extracting prices: {e}", exc_info=True)
            return {
                "success": False,
                "item": item_name,
                "message": f"❌ Gagal memproses hasil pencarian: {str(e)}"
            }

    async def _search_price_fallback(self, item_name: str) -> Dict[str, Any]:
        """
        Fallback price search using simulated database (when MCP unavailable)

        Args:
            item_name: Name of the item to search

        Returns:
            Dict with price information
        """
        logger.info(f"Using fallback price database for: {item_name}")

        # Simulated price database
        price_db = {
            # Electronics
            "laptop": {"min": 3000000, "max": 25000000, "avg": 8000000},
            "iphone": {"min": 8000000, "max": 25000000, "avg": 15000000},
            "ps5": {"min": 7000000, "max": 9000000, "avg": 8000000},
            "samsung": {"min": 2000000, "max": 20000000, "avg": 7000000},
            "macbook": {"min": 12000000, "max": 35000000, "avg": 20000000},
            # Common items
            "sepatu": {"min": 200000, "max": 3000000, "avg": 500000},
            "baju": {"min": 50000, "max": 1000000, "avg": 200000},
            "tas": {"min": 100000, "max": 5000000, "avg": 500000},
            "jam": {"min": 150000, "max": 10000000, "avg": 1000000},
            "headphone": {"min": 100000, "max": 5000000, "avg": 800000},
        }

        # Search for item (case insensitive, partial match)
        item_lower = item_name.lower()
        found_item = None

        for key, value in price_db.items():
            if key in item_lower or item_lower in key:
                found_item = (key, value)
                break

        if found_item:
            key, price_info = found_item
            return {
                "success": True,
                "item": item_name,
                "price_range": {
                    "min": price_info["min"],
                    "max": price_info["max"],
                    "avg": price_info["avg"]
                },
                "source": "Database (Estimated)",
                "message": f"🔍 Perkiraan harga untuk '{item_name}':\n\n" +
                          f"  • Harga terendah: Rp {price_info['min']:,.0f}\n" +
                          f"  • Harga tertinggi: Rp {price_info['max']:,.0f}\n" +
                          f"  • Harga rata-rata: Rp {price_info['avg']:,.0f}\n\n" +
                          "📊 Sumber: Database Estimasi (bukan harga real-time)\n" +
                          "💡 Untuk harga aktual terkini, cek marketplace langsung"
            }
        else:
            return {
                "success": False,
                "item": item_name,
                "message": f"🔍 Maaf, tidak menemukan informasi harga untuk '{item_name}'.\n" +
                          "Coba sebutkan item dengan lebih spesifik (contoh: 'laptop', 'iPhone', 'PS5')"
            }

    # ============================================================================
    # DATABASE TOOLS MCP SERVER
    # ============================================================================

    def analyze_spending_trends(self, transactions: List[Dict]) -> Dict[str, Any]:
        """
        Analyze spending trends and patterns

        Args:
            transactions: List of transaction dictionaries

        Returns:
            Dict with trend analysis
        """
        try:
            if not transactions:
                return {
                    "success": False,
                    "message": "Tidak ada data transaksi untuk dianalisis"
                }

            df = pd.DataFrame(transactions)

            # Convert date column
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')

            # Analyze expenses by month
            expenses = df[df['type'] == 'expense']
            income = df[df['type'] == 'income']

            # Monthly totals
            monthly_expense = expenses.groupby('month')['amount'].sum()
            monthly_income = income.groupby('month')['amount'].sum()

            # Top spending categories
            top_categories = expenses.groupby('category')['amount'].sum().sort_values(ascending=False).head(5)

            # Build report
            report = "📊 **Analisis Tren Pengeluaran:**\n\n"

            # Monthly trends
            if len(monthly_expense) > 1:
                report += "**Tren Bulanan:**\n"
                for month, amount in monthly_expense.items():
                    report += f"  • {month}: Rp {amount:,.0f}\n"
                report += "\n"

            # Top categories
            report += "**Top 5 Kategori Pengeluaran:**\n"
            for idx, (category, amount) in enumerate(top_categories.items(), 1):
                total_expense = expenses['amount'].sum()
                percentage = (amount / total_expense * 100) if total_expense > 0 else 0
                report += f"  {idx}. {category}: Rp {amount:,.0f} ({percentage:.1f}%)\n"

            # Insights
            if len(monthly_expense) > 1:
                trend = "naik" if monthly_expense.iloc[-1] > monthly_expense.iloc[-2] else "turun"
                report += f"\n💡 **Insight:** Pengeluaran bulan ini {trend} dibanding bulan lalu"

            return {
                "success": True,
                "report": report,
                "data": {
                    "monthly_expense": monthly_expense.to_dict(),
                    "top_categories": top_categories.to_dict()
                }
            }

        except Exception as e:
            logger.error(f"Error analyzing trends: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal menganalisis tren: {str(e)}"
            }

    # ============================================================================
    # CALENDAR/REMINDER MCP SERVER
    # ============================================================================

    def _load_reminders(self) -> Dict[str, List[Dict]]:
        """Load reminders from JSON file"""
        try:
            if self.reminders_file.exists():
                with open(self.reminders_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading reminders: {e}")

        return {}

    def _save_reminders(self):
        """Save reminders to JSON file"""
        try:
            with open(self.reminders_file, 'w', encoding='utf-8') as f:
                json.dump(self.reminders, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving reminders: {e}")

    def add_reminder(self, user_id: str, reminder_text: str,
                    due_date: str, category: str = "Tagihan") -> Dict[str, Any]:
        """
        Add a reminder for the user

        Args:
            user_id: User ID
            reminder_text: Reminder description
            due_date: Due date (string format: YYYY-MM-DD or DD)
            category: Reminder category

        Returns:
            Dict with status and message
        """
        try:
            if user_id not in self.reminders:
                self.reminders[user_id] = []

            # Generate reminder ID
            reminder_id = len(self.reminders[user_id]) + 1

            # Parse due date
            try:
                # Try full date format
                parsed_date = datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                try:
                    # Try day-only format (assume current month)
                    day = int(due_date)
                    now = datetime.now()
                    parsed_date = datetime(now.year, now.month, day)
                    # If date has passed, use next month
                    if parsed_date < now:
                        if now.month == 12:
                            parsed_date = datetime(now.year + 1, 1, day)
                        else:
                            parsed_date = datetime(now.year, now.month + 1, day)
                except ValueError:
                    return {
                        "success": False,
                        "message": "❌ Format tanggal tidak valid. Gunakan format: YYYY-MM-DD atau DD (tanggal saja)"
                    }

            # Create reminder
            reminder = {
                "id": reminder_id,
                "text": reminder_text,
                "due_date": parsed_date.strftime("%Y-%m-%d"),
                "category": category,
                "created_at": datetime.now().isoformat(),
                "completed": False
            }

            self.reminders[user_id].append(reminder)
            self._save_reminders()

            logger.info(f"Added reminder for user {user_id}: {reminder_text}")

            return {
                "success": True,
                "reminder_id": reminder_id,
                "message": f"✅ Reminder berhasil ditambahkan!\n" +
                          f"📅 {reminder_text}\n" +
                          f"🗓️ Jatuh tempo: {parsed_date.strftime('%d %B %Y')}\n" +
                          f"🏷️ Kategori: {category}"
            }

        except Exception as e:
            logger.error(f"Error adding reminder: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal menambahkan reminder: {str(e)}"
            }

    def get_reminders(self, user_id: str, include_completed: bool = False) -> Dict[str, Any]:
        """
        Get all reminders for a user

        Args:
            user_id: User ID
            include_completed: Include completed reminders

        Returns:
            Dict with reminders list
        """
        try:
            user_reminders = self.reminders.get(user_id, [])

            if not include_completed:
                user_reminders = [r for r in user_reminders if not r.get('completed', False)]

            if not user_reminders:
                return {
                    "success": True,
                    "reminders": [],
                    "message": "📅 Belum ada reminder yang aktif"
                }

            # Sort by due date
            user_reminders.sort(key=lambda x: x['due_date'])

            # Build message
            message = f"📅 **Reminder Kamu ({len(user_reminders)}):**\n\n"
            for reminder in user_reminders:
                due_date = datetime.strptime(reminder['due_date'], "%Y-%m-%d")
                status = "✅" if reminder.get('completed') else "⏰"
                message += f"{status} [{reminder['id']}] {reminder['text']}\n"
                message += f"   🗓️ {due_date.strftime('%d %B %Y')} | 🏷️ {reminder['category']}\n\n"

            return {
                "success": True,
                "reminders": user_reminders,
                "message": message
            }

        except Exception as e:
            logger.error(f"Error getting reminders: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal mengambil reminder: {str(e)}"
            }

    def complete_reminder(self, user_id: str, reminder_id: int) -> Dict[str, Any]:
        """
        Mark a reminder as completed

        Args:
            user_id: User ID
            reminder_id: Reminder ID

        Returns:
            Dict with status and message
        """
        try:
            user_reminders = self.reminders.get(user_id, [])

            for reminder in user_reminders:
                if reminder['id'] == reminder_id:
                    reminder['completed'] = True
                    reminder['completed_at'] = datetime.now().isoformat()
                    self._save_reminders()

                    return {
                        "success": True,
                        "message": f"✅ Reminder '{reminder['text']}' ditandai selesai!"
                    }

            return {
                "success": False,
                "message": f"❌ Reminder #{reminder_id} tidak ditemukan"
            }

        except Exception as e:
            logger.error(f"Error completing reminder: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal menandai reminder: {str(e)}"
            }

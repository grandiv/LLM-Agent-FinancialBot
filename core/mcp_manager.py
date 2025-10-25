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

    # ============================================================================
    # WEB SEARCH MCP SERVER (Bing -> Brave -> DuckDuckGo)
    # ============================================================================

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
        Extract price information and URLs from Web Search MCP results

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

            logger.info(f"Extracting prices from search results (length: {len(text_content)} chars)")

            # Debug: Log first 2000 chars to understand format
            logger.info(f"MCP result preview (first 2000 chars): {text_content[:2000]}")

            # Price patterns for Indonesian Rupiah
            price_patterns = [
                r'Rp\s*(\d{1,3}(?:\.\d{3})+)',           # Rp 1.000.000
                r'Rp\s*(\d+(?:,\d{3})+)',                 # Rp 1,000,000
                r'Rp\s*(\d{7,})',                         # Rp 1000000
                r'(?:harga|price|mulai)\s*:?\s*Rp\s*(\d{1,3}(?:\.\d{3})+)',
                r'(?:harga|price|mulai)\s*:?\s*Rp\s*(\d+(?:,\d{3})+)',
                r'(?:harga|price|mulai)\s*:?\s*Rp\s*(\d{7,})',
            ]

            # Extract URLs, titles, and prices from the text
            # MCP Format: "**1. Title**\nURL: https://www.bing.com/ck/a?...&u=encoded...\nDescription: ...\n**Full Content:**\n..."

            # Extract titles and URLs together - MCP format uses **Number. Title**
            # Use [\s\S] to match any whitespace including newlines
            title_pattern = r'\*\*(\d+)\.\s*([^\*]+?)\*\*[\s\n]+URL:\s*(https?://[^\s]+)'
            title_url_matches = re.findall(title_pattern, text_content, re.MULTILINE)

            logger.info(f"Found {len(title_url_matches)} title/URL matches")
            if len(title_url_matches) > 0:
                # title_url_matches now contains tuples of (number, title, url)
                logger.info(f"First match example: #{title_url_matches[0][0]} Title='{title_url_matches[0][1].strip()[:50]}...', URL='{title_url_matches[0][2][:80]}...'")
            else:
                # Debug: show what patterns exist
                logger.warning("No matches found. Checking for pattern components...")
                title_only = re.findall(r'\*\*(\d+)\.\s*([^\*]+?)\*\*', text_content)
                url_only = re.findall(r'URL:\s*(https?://[^\s]+)', text_content)
                logger.info(f"Found {len(title_only)} titles and {len(url_only)} URLs separately")

            # Split content by result sections to associate prices with URLs
            # Each result starts with **Number. Title**
            result_sections = re.split(r'\*\*\d+\.\s*[^\*]+?\*\*', text_content)
            logger.info(f"Split into {len(result_sections)} result sections")

            price_sources = []  # List of (price, url, title) tuples
            all_prices = []

            # Extract prices from each result section and associate with URLs and titles
            for i, (number, title, raw_url) in enumerate(title_url_matches):
                # Clean Bing redirect URL to get actual source URL
                url = self._clean_redirect_url(raw_url)

                # Log the cleaning result
                if url != raw_url:
                    logger.info(f"Result {number}: Cleaned URL from Bing redirect")
                    logger.info(f"  Before: {raw_url[:100]}...")
                    logger.info(f"  After:  {url}")
                else:
                    logger.info(f"Result {number}: Direct URL (no redirect)")
                    logger.info(f"  URL: {url}")

                # Get the corresponding content section
                if i + 1 < len(result_sections):
                    section_content = result_sections[i + 1]
                else:
                    continue

                # Extract prices from this section
                section_prices = []
                for pattern in price_patterns:
                    matches = re.findall(pattern, section_content, re.IGNORECASE)
                    for match in matches:
                        price_str = match.replace('.', '').replace(',', '').replace(' ', '')
                        try:
                            price = int(price_str)
                            if 1000 <= price <= 1_000_000_000:
                                section_prices.append(price)
                        except ValueError:
                            continue

                # Log what we found (or didn't find)
                if section_prices:
                    min_section_price = min(section_prices)
                    price_sources.append((min_section_price, url, title.strip()))
                    all_prices.extend(section_prices)
                    logger.info(f"Result #{number}: Found {len(section_prices)} prices (min: Rp {min_section_price:,})")
                else:
                    # Log snippet of content for debugging
                    logger.warning(f"Result #{number}: No prices found in section. Content preview: {section_content[:200]}...")

            # Remove duplicate prices
            all_prices = list(set(all_prices))

            # Sort price sources by price (lowest first)
            price_sources.sort(key=lambda x: x[0])

            logger.info(f"Extracted {len(all_prices)} unique prices from {len(price_sources)} sources")

            if all_prices:
                min_price = min(all_prices)
                max_price = max(all_prices)
                avg_price = sum(all_prices) // len(all_prices)

                # Build message with top 5 sources
                message = f"🔍 **Hasil pencarian harga untuk '{item_name}'** (Real-time via Web Search):\n\n"
                message += f"  • Harga terendah: Rp {min_price:,.0f}\n"
                message += f"  • Harga tertinggi: Rp {max_price:,.0f}\n"
                message += f"  • Harga rata-rata: Rp {avg_price:,.0f}\n"
                message += f"  • Data dari {len(all_prices)} harga, {len(price_sources)} sumber\n\n"

                # Add top 5 sources with titles and URLs
                if price_sources:
                    message += "🔗 **Sumber Harga (Top 5):**\n"
                    for i, (price, url, title) in enumerate(price_sources[:5], 1):
                        # Truncate title if too long
                        display_title = title[:60] + '...' if len(title) > 60 else title
                        message += f"{i}. Rp {price:,.0f} - **{display_title}**\n"
                        message += f"   <{url}>\n"
                    message += "\n"

                message += "📊 Sumber: Web Search MCP (Bing -> Brave -> DuckDuckGo)\n"
                message += "💡 Klik link untuk melihat detail & verifikasi harga"

                return {
                    "success": True,
                    "item": item_name,
                    "price_range": {
                        "min": min_price,
                        "max": max_price,
                        "avg": avg_price
                    },
                    "source": "Web Search MCP (Bing/Brave/DuckDuckGo)",
                    "sample_count": len(all_prices),
                    "sources": price_sources[:5],  # Top 5 sources
                    "message": message
                }
            else:
                return {
                    "success": False,
                    "item": item_name,
                    "message": f"🔍 Pencarian web selesai, tapi tidak menemukan harga spesifik untuk '{item_name}'.\n" +
                              "Coba sebutkan item dengan lebih detail (contoh: 'iPhone 15 Pro', 'Laptop Asus ROG')"
                }

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

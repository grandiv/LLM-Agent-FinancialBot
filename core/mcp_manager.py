"""
MCP (Model Context Protocol) Manager
Manages MCP server connections and tool execution for enhanced agent capabilities
"""

import os
import json
import logging
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import pandas as pd
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)


class MCPManager:
    """Manager for MCP server integrations"""

    def __init__(self, export_dir: str = "exports", reminders_file: str = "reminders.json",
                 web_search_mcp_path: str = "C:\\Projects\\web-search-mcp-v0.3.2\\dist\\index.js"):
        """
        Initialize MCP Manager

        Args:
            export_dir: Directory for exported files
            reminders_file: JSON file to store reminders
            web_search_mcp_path: Path to web-search-mcp server executable
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)

        self.reminders_file = Path(reminders_file)
        self.reminders = self._load_reminders()

        # Web search MCP server configuration
        self.web_search_mcp_path = web_search_mcp_path
        self._web_search_session = None
        self._web_search_client = None

        logger.info("MCP Manager initialized")

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

            # Export to CSV
            df.to_csv(filepath, index=False, encoding='utf-8-sig')

            logger.info(f"Exported CSV for user {user_id}: {filepath}")

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

            # Create Excel writer
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
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

            logger.info(f"Exported Excel for user {user_id}: {filepath}")

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
    # WEB SEARCH MCP SERVER
    # ============================================================================

    async def _init_web_search_client(self):
        """Initialize web search MCP client connection"""
        if self._web_search_session is not None:
            return  # Already initialized

        try:
            logger.info(f"Initializing web-search-mcp client: {self.web_search_mcp_path}")

            # Create server parameters for stdio connection
            server_params = StdioServerParameters(
                command="node",
                args=[self.web_search_mcp_path],
                env=None
            )

            # Create stdio client context
            stdio_transport = stdio_client(server_params)
            self._web_search_client = stdio_transport

            # Initialize session
            read, write = await stdio_transport.__aenter__()
            self._web_search_session = ClientSession(read, write)
            await self._web_search_session.__aenter__()

            logger.info("Web search MCP client initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize web search MCP client: {e}", exc_info=True)
            raise

    async def _cleanup_web_search_client(self):
        """Cleanup web search MCP client connection"""
        try:
            if self._web_search_session:
                await self._web_search_session.__aexit__(None, None, None)
                self._web_search_session = None

            if self._web_search_client:
                await self._web_search_client.__aexit__(None, None, None)
                self._web_search_client = None

            logger.info("Web search MCP client cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up web search client: {e}", exc_info=True)

    def _extract_search_data(self, raw_results: str) -> List[Dict]:
        """
        Extract clean structured data from raw search results for LLM processing

        Args:
            raw_results: Raw text from web search

        Returns:
            List of dicts with title, url, and content snippets
        """
        import re

        lines = raw_results.split('\n')
        results = []
        current_result = {}
        in_content = False

        for line in lines:
            line = line.strip()

            # Skip metadata
            if any(skip in line.lower() for skip in [
                'search completed', 'status:', 'search engine:', 'result requested',
                'successfully extracted', 'failed:', 'results:', 'pdf:'
            ]):
                continue

            # Detect numbered titles
            if re.match(r'\*\*\d+\.\s+.+\*\*$', line):
                if current_result:
                    results.append(current_result)

                # Extract clean title
                title = re.sub(r'\*\*\d+\.\s+', '', line).rstrip('*').strip()
                # Get text after last › or clean up domain parts
                if '›' in title:
                    title = title.split('›')[-1].strip()
                else:
                    # Remove domain/URL parts
                    title = re.sub(r'[a-z0-9\-\.]+\.[a-z]{2,}(\s+›.*?)?', '', title)
                    title = re.sub(r'\s+', ' ', title).strip()

                current_result = {'title': title, 'content': ''}
                in_content = False
                continue

            # Capture URL (clean it if it's a redirect)
            if line.startswith('URL:'):
                url = line.replace('URL:', '').strip()
                # Clean Bing/Google redirects - extract actual URL
                if 'bing.com/ck/a?' in url or 'google.com/url?' in url:
                    # Try to extract real URL from redirect
                    match = re.search(r'&u=a1([^&]+)', url)
                    if match:
                        import urllib.parse
                        try:
                            decoded = urllib.parse.unquote(match.group(1))
                            # Decode the a1 prefix encoding
                            url = decoded.replace('aHR0cHM6Ly', 'https://').replace('aHR0cDovL', 'http://')
                        except:
                            pass  # Keep original if decoding fails

                if current_result:
                    current_result['url'] = url
                continue

            # Mark content start
            if line.startswith('**Full Content:**'):
                in_content = True
                continue

            # Collect content (limited to keep it concise)
            if in_content and current_result and len(current_result.get('content', '')) < 500:
                if not line.startswith('[') and line:  # Skip [Hasil dipotong...]
                    current_result['content'] += line + ' '

        # Add last result
        if current_result:
            results.append(current_result)

        return results

    def _parse_search_results(self, raw_results: str, item_name: str) -> str:
        """
        Parse and format raw search results into user-friendly format

        Args:
            raw_results: Raw text from web search
            item_name: Name of item being searched

        Returns:
            Formatted, user-friendly search results
        """
        import re

        # Extract key information from the raw results
        lines = raw_results.split('\n')

        results = []
        current_result = {}
        skip_content = False

        for line in lines:
            line = line.strip()

            # Skip ALL metadata and status lines
            if any(skip in line.lower() for skip in [
                'search completed', 'status:', 'search engine:', 'result requested',
                'successfully extracted', 'failed:', 'results:', 'pdf:'
            ]):
                continue

            # Detect result number lines (e.g., "**1. Title**")
            if re.match(r'\*\*\d+\.\s+.+\*\*$', line):
                # This is a numbered title
                if current_result:
                    results.append(current_result)

                # Extract title (remove ** and number)
                title = re.sub(r'\*\*\d+\.\s+', '', line).rstrip('*').strip()

                # Method: Extract the ACTUAL headline (usually after the last › or at the end with 2+ spaces)
                # Example: "KOMPAS.com   tekno.kompas.com   › gadget  Harga iPhone..."
                # We want: "Harga iPhone..."

                # First, extract source name (before first domain)
                source = ""
                source_match = re.match(r'([A-Z][A-Za-z0-9\s\.\-]+?)\s+[a-z0-9\-\.]+\.[a-z]{2,}', title)
                if source_match:
                    source = source_match.group(1).strip()

                # Get the actual article title (text with 2+ consecutive capital letters or after last ›)
                main_title = title
                if '›' in title:
                    # Take everything after the last ›
                    main_title = title.split('›')[-1].strip()
                else:
                    # Look for the actual headline (usually has capitalization pattern)
                    # Remove domain patterns first
                    cleaned = re.sub(r'[a-z0-9\-\.]+\.[a-z]{2,}(\s+›\s+[a-z\s&]+)*', '', title)
                    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                    if cleaned:
                        main_title = cleaned

                # Final title: use source if we have it, otherwise just main title
                if source and len(source) < 30:  # Reasonable source name length
                    title = f"{source}: {main_title}"
                else:
                    title = main_title

                # Cleanup and limit length (shorter for link display)
                title = re.sub(r'\s+', ' ', title).strip()
                if len(title) > 70:
                    title = title[:67] + '...'

                current_result = {'title': title}
                skip_content = False
                continue

            # Capture URL lines
            if line.startswith('URL:'):
                url = line.replace('URL:', '').strip()
                if current_result:
                    current_result['url'] = url
                continue

            # Skip Description lines (they're often redundant)
            if line.startswith('Description:'):
                continue

            # Skip separator lines
            if line in ['---', '—']:
                continue

            # Mark start of full content
            if line.startswith('**Full Content:**'):
                skip_content = True  # We'll skip most content, only extract prices
                current_result['has_content'] = True
                continue

            # Extract ONLY price information from content
            if skip_content and current_result.get('has_content'):
                # Look for prices in this line
                price_matches = re.findall(r'Rp\s?[\d.,]+(?:\s?(?:juta|ribu|jutaan))?', line, re.IGNORECASE)
                if price_matches:
                    if 'prices' not in current_result:
                        current_result['prices'] = []
                    current_result['prices'].extend(price_matches[:3])  # Max 3 prices per line

        # Add last result
        if current_result:
            results.append(current_result)

        # Format output - CLEAN SUMMARY with LINKS
        if not results:
            return f"Maaf, tidak menemukan informasi harga untuk '{item_name}' 😔"

        # Collect all prices and create summary
        all_prices = []
        links = []

        for result in results[:5]:  # Process up to 5 results
            title = result.get('title', '').strip()
            prices = result.get('prices', [])
            url = result.get('url', '')

            if prices:
                # Get unique prices from this result
                seen = set()
                unique_prices = []
                for p in prices[:3]:  # Max 3 prices per source
                    p_clean = p.strip()
                    # Extract just the number for comparison
                    price_num = re.sub(r'[^\d]', '', p_clean)
                    if price_num and price_num not in seen:
                        seen.add(price_num)
                        unique_prices.append(p_clean)
                        all_prices.append(price_num)

                # Add to links if we have both title and prices
                if title and unique_prices and url:
                    # Use first price for the link
                    links.append({
                        'price': unique_prices[0],
                        'title': title,
                        'url': url
                    })

        # Calculate price range
        if all_prices:
            price_numbers = [int(p) for p in all_prices if p.isdigit()]
            if price_numbers:
                min_price = min(price_numbers)
                max_price = max(price_numbers)

                # Format prices in millions if >= 1 juta
                def format_price(num):
                    if num >= 1000000:
                        juta = num / 1000000
                        # Round to 1 decimal and remove .0 if whole number
                        juta_rounded = round(juta, 1)
                        if juta_rounded == int(juta_rounded):
                            return f"Rp {int(juta_rounded)} juta"
                        else:
                            return f"Rp {juta_rounded} juta"
                    else:
                        return f"Rp {num:,}"

                min_formatted = format_price(min_price)
                max_formatted = format_price(max_price)

                # Build summary
                source_count = len(links)
                formatted = f"Ditemukan harga **{item_name}** dari {source_count} sumber. "
                formatted += f"Harga mulai dari **{min_formatted}** hingga **{max_formatted}**. "
                formatted += "Perlu diingat bahwa harga dapat berbeda tergantung spesifikasi, toko, dan lokasi.\n\n"

                # Add links
                if links:
                    formatted += "🔗 **Sumber:**\n"
                    for link in links[:5]:  # Show max 5 links
                        formatted += f"• {link['price']} - {link['title']}\n"
                        formatted += f"  {link['url']}\n\n"

                return formatted.strip()

        # Fallback if no prices found
        formatted = f"Ditemukan informasi tentang **{item_name}** dari {len(results)} sumber, "
        formatted += "namun informasi harga spesifik tidak tersedia.\n\n"

        if links:
            formatted += "🔗 **Sumber:**\n"
            for idx, result in enumerate(results[:3], 1):
                title = result.get('title', 'Hasil Pencarian')
                url = result.get('url', '')
                if url:
                    formatted += f"{idx}. {title}\n   {url}\n\n"

        return formatted.strip()

    async def search_price(self, item_name: str, limit: int = 3) -> Dict[str, Any]:
        """
        Search for current price of an item online using web-search-mcp

        Args:
            item_name: Name of the item to search
            limit: Number of search results to return (default: 3)

        Returns:
            Dict with search results and price information (includes raw data for LLM processing)
        """
        try:
            logger.info(f"Searching price for: {item_name}")

            # Initialize MCP client if needed
            await self._init_web_search_client()

            # Construct search query for price information
            search_query = f"{item_name} harga Indonesia price"

            # Call the full-web-search tool
            result = await self._web_search_session.call_tool(
                "full-web-search",
                arguments={
                    "query": search_query,
                    "limit": limit,
                    "includeContent": True,
                    "maxContentLength": 3000  # Get more content for better LLM parsing
                }
            )

            # Extract text content from result
            if hasattr(result, 'content') and len(result.content) > 0:
                search_text = ""
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        search_text += content_item.text + "\n"

                # Extract structured data for LLM to process
                structured_data = self._extract_search_data(search_text)

                # Return raw data for LLM processing in bot_core
                return {
                    "success": True,
                    "item": item_name,
                    "raw_results": search_text,
                    "structured_data": structured_data,
                    "needs_llm_formatting": True
                }
            else:
                return {
                    "success": False,
                    "item": item_name,
                    "message": f"🔍 Maaf, tidak menemukan informasi harga untuk '{item_name}' di hasil pencarian."
                }

        except Exception as e:
            logger.error(f"Error searching price: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal mencari harga: {str(e)}"
            }
        finally:
            # Cleanup client after use to avoid resource leaks
            await self._cleanup_web_search_client()

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

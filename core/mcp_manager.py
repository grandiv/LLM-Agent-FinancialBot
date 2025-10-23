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

    async def search_price(self, item_name: str) -> Dict[str, Any]:
        """
        Search for current price of an item online (simulated)

        Args:
            item_name: Name of the item to search

        Returns:
            Dict with price range and source information
        """
        try:
            # NOTE: In production, this would call actual search APIs
            # For now, we'll simulate price lookup with common items

            logger.info(f"Searching price for: {item_name}")

            # Simulated price database (in production, use real APIs)
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
                    "message": f"🔍 Hasil pencarian harga untuk '{item_name}':\n" +
                              f"  • Harga terendah: Rp {price_info['min']:,.0f}\n" +
                              f"  • Harga tertinggi: Rp {price_info['max']:,.0f}\n" +
                              f"  • Harga rata-rata: Rp {price_info['avg']:,.0f}\n\n" +
                              "💡 Harga bisa bervariasi tergantung spesifikasi dan toko"
                }
            else:
                return {
                    "success": False,
                    "item": item_name,
                    "message": f"🔍 Maaf, tidak menemukan informasi harga untuk '{item_name}'.\n" +
                              "Coba sebutkan item dengan lebih spesifik (contoh: 'laptop', 'iPhone', 'PS5')"
                }

        except Exception as e:
            logger.error(f"Error searching price: {e}", exc_info=True)
            return {
                "success": False,
                "message": f"❌ Gagal mencari harga: {str(e)}"
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

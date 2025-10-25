"""
Core logic bot yang menghubungkan LLM Agent dengan Database
"""

import logging
import asyncio
from typing import Dict, Optional
from .llm_agent import LLMAgent
from .database import DatabaseManager
from .mcp_manager import MCPManager

logger = logging.getLogger(__name__)

class FinancialBotCore:
    """Core bot yang menghandle semua logic bisnis"""

    def __init__(self, llm_agent: LLMAgent, database: DatabaseManager,
                 mcp_manager: Optional[MCPManager] = None):
        """
        Initialize bot core

        Args:
            llm_agent: Instance dari LLMAgent
            database: Instance dari DatabaseManager
            mcp_manager: Instance dari MCPManager (opsional)
        """
        self.llm = llm_agent
        self.db = database
        self.mcp = mcp_manager or MCPManager()

        # Store last price search per user for purchase intent
        self.last_price_search: Dict[str, Dict] = {}  # user_id -> price_search_result

    async def process_message(self, user_id: str, username: str, message: str):
        """
        Proses pesan dari user dan return response

        Args:
            user_id: ID user (Discord ID atau CLI user)
            username: Username user
            message: Pesan dari user

        Returns:
            String response atau Dict dengan 'message' dan 'file_path' untuk file upload
        """
        try:
            # Dapatkan data keuangan user untuk context
            balance_data = self.db.get_user_balance(user_id)
            recent_transactions = self.db.get_user_transactions(user_id, limit=3)

            # Get last price search for purchase intent context
            last_price_search = self.last_price_search.get(user_id)

            # Pre-process message for better intent detection
            message_lower = message.lower()

            # Quick keyword-based intent override for export (LLM struggles with Indonesian "ekspor")
            if any(keyword in message_lower for keyword in ["ekspor", "export", "unduh laporan", "download laporan"]):
                if "excel" in message_lower or "xlsx" in message_lower:
                    # Force export_report intent with excel format
                    result = {
                        "intent": "export_report",
                        "format": "excel",
                        "response_text": "Baik, saya akan ekspor laporan keuangan kamu ke format Excel..."
                    }
                elif "csv" in message_lower:
                    result = {
                        "intent": "export_report",
                        "format": "csv",
                        "response_text": "Baik, saya akan ekspor laporan keuangan kamu ke format CSV..."
                    }
                elif "laporan" in message_lower:
                    # Default to Excel if format not specified
                    result = {
                        "intent": "export_report",
                        "format": "excel",
                        "response_text": "Baik, saya akan ekspor laporan keuangan kamu ke format Excel..."
                    }
                else:
                    # Let LLM handle it
                    result = self.llm.process_message(
                        user_id=user_id,
                        username=username,
                        message=message,
                        balance_data=balance_data,
                        recent_transactions=recent_transactions,
                        last_price_search=last_price_search
                    )
            else:
                # Proses dengan LLM
                result = self.llm.process_message(
                    user_id=user_id,
                    username=username,
                    message=message,
                    balance_data=balance_data,
                    recent_transactions=recent_transactions,
                    last_price_search=last_price_search
                )

            intent = result.get("intent")
            logger.info(f"Processing intent: {intent} for user {user_id}")

            # Handle berdasarkan intent
            if intent == "record_income":
                return self._handle_record_income(user_id, username, result)

            elif intent == "record_expense":
                return self._handle_record_expense(user_id, username, result)

            elif intent == "check_balance":
                return self._handle_check_balance(user_id, result)

            elif intent == "get_report":
                return self._handle_get_report(user_id, result)

            elif intent == "budget_advice":
                return self._handle_budget_advice(user_id, result, balance_data)

            elif intent == "purchase_analysis":
                return self._handle_purchase_analysis(user_id, result, balance_data)

            elif intent == "purchase_item":
                return self._handle_purchase_item(user_id, username, result)

            elif intent == "delete_transaction":
                return self._handle_delete_transaction(user_id, result)

            # MCP-enabled intents
            elif intent == "export_report":
                return self._handle_export_report(user_id, result)

            elif intent == "web_search":
                return await self._handle_web_search(result, message)

            elif intent == "search_price":
                return await self._handle_search_price(result, user_id)

            elif intent == "analyze_trends":
                return self._handle_analyze_trends(user_id, result)

            elif intent == "set_reminder":
                return self._handle_set_reminder(user_id, result)

            elif intent == "view_reminders":
                return self._handle_view_reminders(user_id, result)

            elif intent == "complete_reminder":
                return self._handle_complete_reminder(user_id, result)

            elif intent == "help":
                return self._handle_help(result)

            elif intent == "casual_chat":
                response = result.get("response_text", "").strip()
                return response if response else "Halo! Ada yang bisa saya bantu? 😊"

            elif intent == "error":
                response = result.get("response_text", "").strip()
                return response if response else "Maaf, ada kesalahan sistem. Coba lagi ya!"

            else:
                response = result.get("response_text", "").strip()
                return response if response else "Maaf, saya kurang mengerti. Bisa dijelaskan lagi? 🤔"

        except Exception as e:
            logger.error(f"Error in process_message: {e}", exc_info=True)
            return "Maaf, terjadi kesalahan. Coba lagi ya! 🙏"

    def _handle_record_income(self, user_id: str, username: str, result: Dict) -> str:
        """Handle pencatatan pemasukan"""
        amount = result.get("amount", 0)
        category = result.get("category", "Lainnya")
        description = result.get("description", "")
        base_response = result.get("response_text", "")

        if amount <= 0:
            return "Maaf, jumlah pemasukan harus lebih dari 0. Coba lagi ya! 💰"

        # Simpan ke database
        success = self.db.add_transaction(
            user_id=user_id,
            username=username,
            transaction_type="income",
            amount=amount,
            category=category,
            description=description
        )

        if success:
            # Dapatkan saldo terbaru
            balance_data = self.db.get_user_balance(user_id)

            # Creative response based on amount and category
            celebration = ""
            if amount >= 10_000_000:
                celebration = "🎉 Wah luar biasa! Pemasukan segede ini jarang-jarang! "
            elif amount >= 5_000_000:
                celebration = "🎊 Mantap banget! Rejeki lancar nih! "
            elif amount >= 1_000_000:
                celebration = "✨ Alhamdulillah, rezeki yang cukup besar! "
            else:
                celebration = "👍 Bagus! Setiap pemasukan itu berarti! "

            # Category-specific encouragement
            if category == "Gaji":
                celebration += "Gaji udah masuk, jangan lupa sisihkan buat tabungan ya! 💪"
            elif category == "Freelance":
                celebration += "Keren, hasil kerja keras kamu! Keep hustling! 🚀"
            elif category == "Investasi":
                celebration += "Smart move! Uang kamu bekerja untuk kamu! 📈"
            elif category == "Hadiah":
                celebration += "Lucky you! Semoga makin banyak rezeki nomplok! 🎁"
            else:
                celebration += "Terus tingkatkan pemasukan kamu! 💪"

            balance_info = f"\n\n💰 Saldo kamu sekarang: Rp {balance_data['balance']:,.0f}"

            # Add extra motivation if balance is good
            if balance_data['balance'] >= 10_000_000:
                balance_info += "\n🌟 Saldo kamu udah sehat banget! Pertahankan ya!"
            elif balance_data['balance'] >= 5_000_000:
                balance_info += "\n💪 Saldo kamu cukup bagus nih! Keep it up!"

            return celebration + balance_info
        else:
            return "Maaf, gagal menyimpan data pemasukan. Coba lagi ya! 🔧"

    def _handle_record_expense(self, user_id: str, username: str, result: Dict) -> str:
        """Handle pencatatan pengeluaran"""
        amount = result.get("amount", 0)
        category = result.get("category", "Lainnya")
        description = result.get("description", "")
        base_response = result.get("response_text", "")

        if amount <= 0:
            return "Maaf, jumlah pengeluaran harus lebih dari 0. Coba lagi ya! 💸"

        # Simpan ke database
        success = self.db.add_transaction(
            user_id=user_id,
            username=username,
            transaction_type="expense",
            amount=amount,
            category=category,
            description=description
        )

        if success:
            # Dapatkan saldo terbaru
            balance_data = self.db.get_user_balance(user_id)
            balance = balance_data['balance']

            # Creative response based on category and amount
            acknowledgment = ""
            if category == "Makanan":
                if amount >= 100_000:
                    acknowledgment = "🍽️ Wah makan enak nih! Semoga kenyang dan worth it ya! "
                else:
                    acknowledgment = "🍽️ Dicatat! Jangan lupa makan bergizi ya! "
            elif category == "Transport":
                acknowledgment = "🚗 Oke, biaya transportasi sudah dicatat! Stay safe on the road! "
            elif category == "Hiburan":
                if amount >= 500_000:
                    acknowledgment = "🎬 Wih, hiburan mahal nih! Semoga seru dan happy ya! "
                else:
                    acknowledgment = "🎬 Have fun! Me time itu penting kok! "
            elif category == "Belanja":
                if amount >= 1_000_000:
                    acknowledgment = "🛍️ Belanja besar nih! Belanja kebutuhan atau keinginan nih? 🤔 "
                else:
                    acknowledgment = "🛍️ Oke, belanja sudah dicatat! Belanja smart ya! "
            elif category == "Tagihan":
                acknowledgment = "📝 Good job! Bayar tagihan tepat waktu itu penting! "
            elif category == "Kesehatan":
                acknowledgment = "🏥 Kesehatan nomor satu! Investasi yang tepat! "
            elif category == "Pendidikan":
                acknowledgment = "📚 Keren! Investasi ke diri sendiri itu yang terbaik! "
            else:
                acknowledgment = "✅ Oke, pengeluaran sudah dicatat! "

            balance_info = f"\n\n💰 Saldo kamu sekarang: Rp {balance:,.0f}"

            # Warning jika saldo negatif
            if balance < 0:
                balance_info += "\n⚠️ Perhatian: Saldo kamu sudah negatif! Waktunya hustle cari pemasukan tambahan! 💪"
            # Warning jika pengeluaran > 80% dari pemasukan
            elif balance_data['income'] > 0 and balance_data['expense'] / balance_data['income'] > 0.8:
                balance_info += "\n⚠️ Pengeluaran kamu sudah lebih dari 80% pemasukan. Mulai hemat atau cari pemasukan tambahan ya! 🎯"
            # Positive reinforcement jika spending masih sehat
            elif balance_data['income'] > 0 and balance_data['expense'] / balance_data['income'] < 0.5:
                balance_info += "\n✨ Bagus! Pengeluaran kamu masih terkontrol kok! Keep it up! 👍"

            return acknowledgment + balance_info
        else:
            return "Maaf, gagal menyimpan data pengeluaran. Coba lagi ya! 🔧"

    def _handle_check_balance(self, user_id: str, result: Dict) -> str:
        """Handle pengecekan saldo"""
        balance_data = self.db.get_user_balance(user_id)

        # Creative opening based on balance
        if balance_data['balance'] >= 10_000_000:
            opening = "🌟 Wah, kondisi finansial kamu sehat banget! Cek deh:\n\n"
        elif balance_data['balance'] >= 1_000_000:
            opening = "💪 Lumayan nih, keep going! Ini ringkasan keuangan kamu:\n\n"
        elif balance_data['balance'] > 0:
            opening = "👍 Oke, masih ada saldo! Ini ringkasannya:\n\n"
        elif balance_data['balance'] == 0:
            opening = "😅 Hmm, lagi tipis nih. Cek dulu ya:\n\n"
        else:
            opening = "⚠️ Uh-oh, perlu perhatian nih! Cek kondisinya:\n\n"

        response = opening + f"""📊 **Ringkasan Keuangan Kamu**

💵 Total Pemasukan: Rp {balance_data['income']:,.0f}
💸 Total Pengeluaran: Rp {balance_data['expense']:,.0f}
💰 Saldo Saat Ini: Rp {balance_data['balance']:,.0f}
"""

        # Tambahkan insight yang lebih kreatif
        if balance_data['balance'] < 0:
            response += "\n⚠️ **Alert!** Saldo kamu negatif! Saatnya action:\n"
            response += "   • Kurangi pengeluaran non-esensial\n"
            response += "   • Cari side hustle atau pemasukan tambahan\n"
            response += "   • Review semua subscription yang tidak perlu"
        elif balance_data['balance'] == 0:
            response += "\n💡 Saldo kamu pas-pasan nih! Tips:\n"
            response += "   • Mulai sisihkan minimal 10% dari pemasukan\n"
            response += "   • Buat pos-pos pengeluaran yang jelas\n"
            response += "   • Cari peluang pemasukan tambahan"
        else:
            savings_percentage = (balance_data['balance'] / balance_data['income'] * 100) if balance_data['income'] > 0 else 0
            if savings_percentage >= 30:
                response += f"\n🏆 **Outstanding!** Kamu udah sisihkan {savings_percentage:.0f}% dari pemasukan!\n"
                response += "   Ini jauh di atas standar 20%. Financial goal on point! 🎯"
            elif savings_percentage >= 20:
                response += f"\n✨ **Great job!** Kamu udah sisihkan {savings_percentage:.0f}% dari pemasukan!\n"
                response += "   Target 20% tercapai! Coba tingkatkan jadi 30% kalau bisa ya! 💪"
            elif savings_percentage >= 10:
                response += f"\n👍 Lumayan! Kamu udah sisihkan {savings_percentage:.0f}% dari pemasukan.\n"
                response += "   Coba tingkatkan jadi minimal 20% buat masa depan yang lebih secure ya!"
            else:
                response += f"\n💡 Saldo kamu {savings_percentage:.0f}% dari pemasukan. Target ideal: minimal 20%!\n"
                response += "   Tips: Pakai metode 50/30/20 (50% kebutuhan, 30% keinginan, 20% tabungan)"

        return response

    def _handle_get_report(self, user_id: str, result: Dict) -> str:
        """Handle permintaan laporan"""
        balance_data = self.db.get_user_balance(user_id)
        category_report = self.db.get_category_report(user_id)
        recent_trans = self.db.get_user_transactions(user_id, limit=5)

        response = f"""📊 **Laporan Keuangan Lengkap**

💰 **Ringkasan:**
- Total Pemasukan: Rp {balance_data['income']:,.0f}
- Total Pengeluaran: Rp {balance_data['expense']:,.0f}
- Saldo: Rp {balance_data['balance']:,.0f}

"""

        # Laporan per kategori
        if category_report:
            response += "📂 **Per Kategori:**\n"
            for category, amounts in sorted(category_report.items(), key=lambda x: x[1]['expense'] + x[1]['income'], reverse=True)[:5]:
                if amounts['income'] > 0:
                    response += f"- {category} (Pemasukan): Rp {amounts['income']:,.0f}\n"
                if amounts['expense'] > 0:
                    response += f"- {category} (Pengeluaran): Rp {amounts['expense']:,.0f}\n"

        # Transaksi terakhir
        if recent_trans:
            response += "\n📝 **5 Transaksi Terakhir:**\n"
            for t in recent_trans:
                trans_type = "➕" if t['type'] == 'income' else "➖"
                response += f"{trans_type} Rp {t['amount']:,.0f} - {t['category']} ({t['description']})\n"

        return response

    def _handle_budget_advice(self, user_id: str, result: Dict, balance_data: Dict) -> str:
        """Handle permintaan saran anggaran (dikombinasikan dengan LLM response)"""
        base_response = result.get("response_text", "")

        # Tambahkan analisis konkret dengan opening yang engaging
        advice = "\n\n💡 **Saran Anggaran dari FinancialBot:**\n"

        if balance_data['balance'] <= 0:
            advice += "\n🚨 **Mode Darurat - Immediate Action Required!**\n"
            advice += "• Prioritas #1: STOP pengeluaran non-esensial sekarang!\n"
            advice += "• Review semua subscription dan batalkan yang tidak perlu\n"
            advice += "• Cari pemasukan tambahan (freelance, jual barang tidak terpakai)\n"
            advice += "• Fokus bayar tagihan penting dulu (listrik, internet, dll)\n"
        else:
            advice += "\n📊 **Rekomendasi Alokasi Saldo (Metode 50/30/20 modified):**\n"

            # Dana darurat (20% dari saldo)
            emergency_fund = balance_data['balance'] * 0.20
            advice += f"\n🏥 Dana Darurat (20%): Rp {emergency_fund:,.0f}"
            advice += f"\n   → Simpan di tempat aman, jangan dipakai kecuali darurat!"

            # Tabungan/Investasi (30% dari saldo)
            savings = balance_data['balance'] * 0.30
            advice += f"\n\n💎 Tabungan/Investasi (30%): Rp {savings:,.0f}"
            advice += f"\n   → Untuk tujuan jangka panjang (DP rumah, pensiun, dll)"

            # Budget harian/kebutuhan (50% dari saldo)
            for_expenses = balance_data['balance'] * 0.50
            advice += f"\n\n🛒 Budget Kebutuhan (50%): Rp {for_expenses:,.0f}"
            advice += f"\n   → Makan, transport, tagihan, kebutuhan sehari-hari"

        # Cek spending ratio dengan message yang lebih engaging
        if balance_data['income'] > 0:
            spending_ratio = balance_data['expense'] / balance_data['income']
            advice += f"\n\n📈 **Analisis Spending Ratio:**"
            if spending_ratio > 0.9:
                advice += f"\n🔴 Kritis! {spending_ratio*100:.0f}% dari pemasukan habis!"
                advice += f"\n   Target sehat: max 70%. Kurangi {(spending_ratio-0.7)*balance_data['income']:,.0f} per bulan!"
            elif spending_ratio > 0.8:
                advice += f"\n🟠 Warning! {spending_ratio*100:.0f}% dari pemasukan habis!"
                advice += f"\n   Hampir batas aman. Coba kurangi pengeluaran atau tambah pemasukan."
            elif spending_ratio > 0.7:
                advice += f"\n🟡 {spending_ratio*100:.0f}% dari pemasukan terpakai."
                advice += f"\n   Masih oke, tapi jangan sampai naik ya!"
            else:
                advice += f"\n🟢 Sehat! {spending_ratio*100:.0f}% dari pemasukan terpakai."
                advice += f"\n   Perfect! Keep maintaining this ratio! 💪"

        return base_response + advice

    def _handle_purchase_analysis(self, user_id: str, result: Dict, balance_data: Dict) -> str:
        """Handle analisis kemampuan beli"""
        item_name = result.get("item_name", "barang tersebut")
        price = result.get("amount", 0)
        base_response = result.get("response_text", "")

        # If price not specified, try to search online
        if price <= 0:
            logger.info(f"Price not specified, searching online for {item_name}")
            try:
                # Try to get existing loop
                try:
                    loop = asyncio.get_running_loop()
                    # If we're already in an async context, create a task
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self.mcp.search_price(item_name))
                        search_result = future.result()
                except RuntimeError:
                    # No running loop, safe to use asyncio.run
                    search_result = asyncio.run(self.mcp.search_price(item_name))
            except Exception as e:
                logger.error(f"Error in price search: {e}", exc_info=True)
                return "Maaf, harga barang harus disebutkan ya! Coba lagi dengan format yang lebih jelas. 💰"

            if search_result["success"]:
                price = search_result["price_range"]["avg"]
                base_response = f"Saya cari harga {item_name} online dulu ya...\n\n" + search_result["message"] + "\n\n"
                base_response += f"Saya akan analisis berdasarkan harga rata-rata: Rp {price:,.0f}\n"
            else:
                return "Maaf, harga barang harus disebutkan ya! Coba lagi dengan format yang lebih jelas. 💰"

        analysis = f"\n\n🛍️ **Analisis Pembelian {item_name}:**\n"
        analysis += f"Harga: Rp {price:,.0f}\n"
        analysis += f"Saldo kamu: Rp {balance_data['balance']:,.0f}\n\n"

        if balance_data['balance'] >= price:
            remaining = balance_data['balance'] - price
            percentage = (price / balance_data['balance']) * 100

            if percentage <= 30:
                analysis += f"✅ Aman dibeli! Sisa saldo: Rp {remaining:,.0f} ({100-percentage:.0f}% dari saldo kamu)\n"
                analysis += "💡 Saran: Pastikan masih ada dana darurat ya!"
            elif percentage <= 60:
                analysis += f"⚠️ Bisa dibeli tapi hati-hati. Sisa saldo: Rp {remaining:,.0f}\n"
                analysis += "💡 Saran: Pertimbangkan apakah ini kebutuhan atau keinginan?"
            else:
                analysis += f"🤔 Kurang disarankan. Sisa saldo cuma: Rp {remaining:,.0f}\n"
                analysis += "💡 Saran: Tunda dulu atau cari alternatif yang lebih murah?"
        else:
            shortage = price - balance_data['balance']
            analysis += f"❌ Belum mampu. Kurang: Rp {shortage:,.0f}\n\n"

            # Hitung berapa bulan harus nabung (asumsi saving 30% dari income per bulan)
            if balance_data['income'] > 0:
                monthly_income = balance_data['income']  # Asumsi total income adalah per bulan
                monthly_savings = monthly_income * 0.30
                if monthly_savings > 0:
                    months_needed = shortage / monthly_savings
                    analysis += f"💡 Jika menabung 30% dari pemasukan (Rp {monthly_savings:,.0f}/bulan),\n"
                    analysis += f"   kamu perlu {months_needed:.1f} bulan untuk bisa beli ini.\n\n"

            analysis += "🎯 Alternatif:\n"
            analysis += f"- Cari yang lebih murah (budget: Rp {balance_data['balance']:,.0f})\n"
            analysis += "- Nabung dulu sambil cari promo/diskon\n"
            analysis += "- Pertimbangkan beli second/bekas\n"

        return base_response + analysis

    def _handle_purchase_item(self, user_id: str, username: str, result: Dict) -> str:
        """Handle pembelian item setelah price search"""
        base_response = result.get("response_text", "")

        # Get last price search from memory
        last_search = self.last_price_search.get(user_id)

        if not last_search or not last_search.get("success"):
            return "Maaf, saya tidak ingat kamu baru cari harga apa. Coba cari harga dulu ya dengan \"cari harga [nama barang]\" 🔍"

        # Extract item details from last search
        item_name = last_search.get("item", "barang")
        price_range = last_search.get("price_range", {})
        sources = last_search.get("sources", [])

        # Check if user specified a source index (option number)
        source_index = result.get("source_index")

        amount = None
        source_info = ""

        if source_index is not None and sources:
            # User chose a specific option (e.g., "mau beli yg 3")
            try:
                if source_index == -1:
                    # -1 means the most expensive (last one)
                    source_index = len(sources)

                # Convert to 0-based index
                idx = source_index - 1

                if 0 <= idx < len(sources):
                    # sources format: (price, url, title)
                    source_data = sources[idx]
                    amount = source_data[0]  # price
                    source_title = source_data[2] if len(source_data) > 2 else "sumber pilihan"
                    source_info = f" dari {source_title}"
                else:
                    return f"Maaf, pilihan nomor {source_index} tidak tersedia. Hanya ada {len(sources)} pilihan. 🔍"
            except Exception as e:
                logger.error(f"Error getting source by index: {e}")
                amount = None

        # Fallback: Check if user specified amount explicitly
        if not amount:
            amount = result.get("amount")

        # Final fallback: use lowest price
        if not amount or amount <= 0:
            amount = price_range.get("min", price_range.get("avg", 0))

        if amount <= 0:
            return "Maaf, ada masalah dengan data harga. Coba cari harga lagi ya! 🔍"

        # Determine category (default to Belanja)
        category = result.get("category", "Belanja")

        # Create description with source info
        description = result.get("description", f"{item_name} (dibeli online)")
        if source_info:
            description = f"{item_name}{source_info}"

        # Record the expense
        success = self.db.add_transaction(
            user_id=user_id,
            username=username,
            transaction_type="expense",
            amount=amount,
            category=category,
            description=description
        )

        if success:
            # Clear the last price search since it's been used
            self.last_price_search.pop(user_id, None)

            # Get updated balance
            balance = self.db.get_user_balance(user_id)

            response = f"✅ Pembelian berhasil dicatat!\n\n"
            response += f"🛍️ Item: {item_name}\n"
            response += f"💰 Harga: Rp {amount:,.0f}\n"
            if source_info:
                response += f"🔗 Dibeli{source_info}\n"
            response += f"📁 Kategori: {category}\n"
            response += f"📝 Keterangan: {description}\n\n"
            response += f"💵 Saldo kamu sekarang: Rp {balance['balance']:,.0f}\n"

            # Add sources if available
            sources = last_search.get("sources", [])
            if sources and len(sources) > 0:
                response += f"\n🔗 Dibeli dari: "
                # Find the source with matching price
                matching_source = next((s for s in sources if s[0] == amount), sources[0])
                if matching_source and len(matching_source) > 1:
                    response += f"{matching_source[1]}"  # URL

            return response
        else:
            return "❌ Gagal mencatat pembelian. Coba lagi ya!"

    def _handle_delete_transaction(self, user_id: str, result: Dict) -> str:
        """Handle penghapusan transaksi"""
        transaction_id = result.get("transaction_id")

        if not transaction_id:
            return "Maaf, ID transaksi tidak ditemukan. Sebutkan ID transaksi yang ingin dihapus ya! 🔢"

        success = self.db.delete_transaction(user_id, transaction_id)

        if success:
            return f"✅ Transaksi #{transaction_id} berhasil dihapus!"
        else:
            return f"❌ Transaksi #{transaction_id} tidak ditemukan atau bukan milik kamu."

    def _handle_help(self, result: Dict) -> str:
        """Handle permintaan bantuan"""
        return """🤖 **FinancialBot - Asisten Keuangan Pribadimu**

Aku bisa bantu kamu:
1. 💵 Mencatat pemasukan
   Contoh: "aku dapat gaji 5 juta", "dapet bonus 1jt"

2. 💸 Mencatat pengeluaran
   Contoh: "habis 50rb buat makan", "beli baju 200 ribu"

3. 💰 Cek saldo
   Contoh: "berapa saldo aku?", "cek balance"

4. 📊 Lihat laporan
   Contoh: "tampilkan laporan", "lihat transaksi terakhir"

5. 💡 Saran anggaran
   Contoh: "kasih saran budget", "gimana ngatur keuangan?"

6. 🛍️ Analisis pembelian
   Contoh: "aku mau beli laptop 15 juta", "mampu ga beli PS5 8jt?"

7. 🗑️ Hapus transaksi
   Contoh: "hapus transaksi 123"

Ngobrol aja dengan natural, aku akan mengerti! 😊
"""

    # ============================================================================
    # MCP HANDLERS
    # ============================================================================

    def _handle_export_report(self, user_id: str, result: Dict) -> Dict:
        """Handle ekspor laporan ke file

        Returns:
            Dict with 'message' and optionally 'file_path' for Discord upload
        """
        export_format = result.get("format", "csv").lower()
        base_response = result.get("response_text", "")

        # Dapatkan data yang diperlukan
        transactions = self.db.get_user_transactions(user_id, limit=1000)
        balance_data = self.db.get_user_balance(user_id)

        if export_format == "excel":
            category_report = self.db.get_category_report(user_id)
            mcp_result = self.mcp.export_to_excel(user_id, transactions, balance_data, category_report)
        else:
            mcp_result = self.mcp.export_to_csv(user_id, transactions, balance_data)

        if mcp_result["success"]:
            message = base_response + "\n\n" + mcp_result["message"] if base_response else mcp_result["message"]
            file_path = mcp_result.get("file_path")
            logger.info(f"Export successful! File path: {file_path}")
            return {
                "message": message,
                "file_path": file_path
            }
        else:
            logger.warning(f"Export failed: {mcp_result['message']}")
            return {"message": mcp_result["message"]}

    async def _handle_web_search(self, result: Dict, original_message: str = "") -> str:
        """Handle general web search for any information"""
        search_query = result.get("search_query", "").strip()
        base_response = result.get("response_text", "").strip()

        # If search_query is missing, try to use original message as fallback
        if not search_query:
            if original_message:
                search_query = original_message
                logger.info(f"search_query empty, using original message: {original_message}")
            else:
                # If still no query, return natural response asking for clarification
                return base_response if base_response else "Hmm, saya kurang mengerti apa yang ingin kamu cari. Bisa dijelaskan lebih spesifik? 🔍"

        try:
            mcp_result = await asyncio.wait_for(
                self.mcp.web_search(search_query),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            return "Pencarian memakan waktu terlalu lama. Coba query yang lebih spesifik ya!"
        except Exception as e:
            logger.error(f"Error in web_search: {e}", exc_info=True)
            return "Maaf, terjadi kesalahan saat mencari informasi. Coba lagi ya! 🔍"

        if mcp_result["success"]:
            return base_response + "\n\n" + mcp_result["message"] if base_response else mcp_result["message"]
        else:
            return mcp_result["message"]

    async def _handle_search_price(self, result: Dict, user_id: str = None) -> str:
        """Handle pencarian harga barang online"""
        item_name = result.get("item_name", "")
        base_response = result.get("response_text", "")

        if not item_name:
            return "Maaf, sebutkan nama barang yang ingin dicari harganya ya! 🔍"

        # Run async search directly (we're in an async context now)
        try:
            # Add timeout to prevent long waits
            mcp_result = await asyncio.wait_for(
                self.mcp.search_price(item_name),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            logger.warning("Search timed out after 30 seconds, using database fallback")
            # Return database fallback immediately
            mcp_result = await self.mcp._search_price_fallback(item_name)
        except Exception as e:
            logger.error(f"Error in search_price: {e}", exc_info=True)
            return "Maaf, terjadi kesalahan saat mencari harga. Coba lagi ya! 🔍"

        # Store the price search result for potential purchase
        if user_id and mcp_result.get("success"):
            self.last_price_search[user_id] = mcp_result
            logger.info(f"Stored price search for user {user_id}: {item_name}")

        if mcp_result["success"]:
            response = base_response + "\n\n" + mcp_result["message"] if base_response else mcp_result["message"]
            # Add helpful hint about purchasing
            response += "\n\n💡 Kalau mau beli, bilang aja \"aku mau beli\" dan saya bantu catat pengeluarannya!"
            return response
        else:
            return mcp_result["message"]

    def _handle_analyze_trends(self, user_id: str, result: Dict) -> str:
        """Handle analisis tren pengeluaran"""
        base_response = result.get("response_text", "")

        # Dapatkan semua transaksi untuk analisis
        transactions = self.db.get_user_transactions(user_id, limit=1000)

        mcp_result = self.mcp.analyze_spending_trends(transactions)

        if mcp_result["success"]:
            return base_response + "\n\n" + mcp_result["report"]
        else:
            return mcp_result["message"]

    def _handle_set_reminder(self, user_id: str, result: Dict) -> str:
        """Handle pembuatan reminder"""
        reminder_text = result.get("reminder_text", "")
        due_date = result.get("due_date", "")
        category = result.get("category", "Tagihan")
        base_response = result.get("response_text", "")

        if not reminder_text or not due_date:
            return "Maaf, sebutkan reminder dan tanggalnya ya! Contoh: 'ingatkan bayar listrik tanggal 5' 📅"

        mcp_result = self.mcp.add_reminder(user_id, reminder_text, due_date, category)

        if mcp_result["success"]:
            return base_response + "\n\n" + mcp_result["message"]
        else:
            return mcp_result["message"]

    def _handle_view_reminders(self, user_id: str, result: Dict) -> str:
        """Handle tampilkan daftar reminder"""
        mcp_result = self.mcp.get_reminders(user_id)
        return mcp_result["message"]

    def _handle_complete_reminder(self, user_id: str, result: Dict) -> str:
        """Handle tandai reminder selesai"""
        reminder_id = result.get("reminder_id")

        if not reminder_id:
            return "Maaf, sebutkan ID reminder yang ingin ditandai selesai ya! 🔢"

        mcp_result = self.mcp.complete_reminder(user_id, reminder_id)
        return mcp_result["message"]

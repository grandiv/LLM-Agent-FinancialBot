"""
Core logic bot yang menghubungkan LLM Agent dengan Database
"""

import logging
from typing import Dict, Optional
from .llm_agent import LLMAgent
from .database import DatabaseManager

logger = logging.getLogger(__name__)

class FinancialBotCore:
    """Core bot yang menghandle semua logic bisnis"""

    def __init__(self, llm_agent: LLMAgent, database: DatabaseManager):
        """
        Initialize bot core

        Args:
            llm_agent: Instance dari LLMAgent
            database: Instance dari DatabaseManager
        """
        self.llm = llm_agent
        self.db = database

    def process_message(self, user_id: str, username: str, message: str) -> str:
        """
        Proses pesan dari user dan return response

        Args:
            user_id: ID user (Discord ID atau CLI user)
            username: Username user
            message: Pesan dari user

        Returns:
            String response untuk dikirim ke user
        """
        try:
            # Dapatkan data keuangan user untuk context
            balance_data = self.db.get_user_balance(user_id)
            recent_transactions = self.db.get_user_transactions(user_id, limit=3)

            # Proses dengan LLM
            result = self.llm.process_message(
                user_id=user_id,
                username=username,
                message=message,
                balance_data=balance_data,
                recent_transactions=recent_transactions
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

            elif intent == "delete_transaction":
                return self._handle_delete_transaction(user_id, result)

            elif intent == "help":
                return self._handle_help(result)

            elif intent == "casual_chat":
                return result.get("response_text", "Halo! Ada yang bisa saya bantu?")

            elif intent == "error":
                return result.get("response_text", "Maaf, ada kesalahan sistem. Coba lagi ya!")

            else:
                return result.get("response_text", "Maaf, saya kurang mengerti. Bisa dijelaskan lagi? 🤔")

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
            balance_info = f"\n\n💰 Saldo kamu sekarang: Rp {balance_data['balance']:,.0f}"
            return base_response + balance_info
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

            balance_info = f"\n\n💰 Saldo kamu sekarang: Rp {balance:,.0f}"

            # Warning jika saldo negatif
            if balance < 0:
                balance_info += "\n⚠️ Perhatian: Saldo kamu sudah negatif! Hati-hati ya!"
            # Warning jika pengeluaran > 80% dari pemasukan
            elif balance_data['income'] > 0 and balance_data['expense'] / balance_data['income'] > 0.8:
                balance_info += "\n⚠️ Pengeluaran kamu sudah lebih dari 80% pemasukan. Mulai hemat ya!"

            return base_response + balance_info
        else:
            return "Maaf, gagal menyimpan data pengeluaran. Coba lagi ya! 🔧"

    def _handle_check_balance(self, user_id: str, result: Dict) -> str:
        """Handle pengecekan saldo"""
        balance_data = self.db.get_user_balance(user_id)

        response = f"""📊 **Ringkasan Keuangan Kamu**

💵 Total Pemasukan: Rp {balance_data['income']:,.0f}
💸 Total Pengeluaran: Rp {balance_data['expense']:,.0f}
💰 Saldo Saat Ini: Rp {balance_data['balance']:,.0f}
"""

        # Tambahkan insight
        if balance_data['balance'] < 0:
            response += "\n⚠️ Saldo kamu negatif! Sebaiknya kurangi pengeluaran ya."
        elif balance_data['balance'] == 0:
            response += "\n💡 Saldo kamu pas-pasan nih. Mulai nabung yuk!"
        else:
            savings_percentage = (balance_data['balance'] / balance_data['income'] * 100) if balance_data['income'] > 0 else 0
            if savings_percentage >= 20:
                response += f"\n✨ Keren! Kamu sudah menyisihkan {savings_percentage:.0f}% dari pemasukan!"
            else:
                response += "\n💡 Coba sisihkan minimal 20% dari pemasukan untuk tabungan ya!"

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

        # Tambahkan analisis konkret
        advice = "\n\n💡 **Saran Anggaran:**\n"

        if balance_data['balance'] <= 0:
            advice += "- 🚨 Prioritas: Kurangi pengeluaran segera!\n"
            advice += "- Cek kategori pengeluaran terbesar dan cari cara menguranginya\n"
        else:
            # Dana darurat (15% dari saldo)
            emergency_fund = balance_data['balance'] * 0.15
            advice += f"- Dana Darurat (15%): Sisihkan Rp {emergency_fund:,.0f}\n"

            # Tabungan (30% dari sisa)
            remaining = balance_data['balance'] - emergency_fund
            savings = remaining * 0.30
            advice += f"- Tabungan (30%): Sisihkan Rp {savings:,.0f}\n"

            # Sisanya untuk kebutuhan
            for_expenses = remaining - savings
            advice += f"- Untuk kebutuhan: Rp {for_expenses:,.0f}\n"

        # Cek spending ratio
        if balance_data['income'] > 0:
            spending_ratio = balance_data['expense'] / balance_data['income']
            if spending_ratio > 0.8:
                advice += "\n⚠️ Pengeluaran kamu sudah {:.0f}% dari pemasukan! Target ideal: max 70%".format(spending_ratio * 100)

        return base_response + advice

    def _handle_purchase_analysis(self, user_id: str, result: Dict, balance_data: Dict) -> str:
        """Handle analisis kemampuan beli"""
        item_name = result.get("item_name", "barang tersebut")
        price = result.get("amount", 0)
        base_response = result.get("response_text", "")

        if price <= 0:
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

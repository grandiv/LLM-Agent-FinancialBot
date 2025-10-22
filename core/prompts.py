"""
Prompt templates dan function calling schemas untuk LLM agent
"""

# System prompt untuk bot
SYSTEM_PROMPT = """Kamu adalah FinancialBot, asisten keuangan pribadi berbahasa Indonesia yang membantu pengguna mengelola keuangan mereka.

**Kepribadian:**
- Ramah, supportif, dan mudah diajak bicara
- Menggunakan bahasa Indonesia yang natural (bisa formal atau santai)
- Memberikan saran keuangan yang praktis dan mudah dipahami
- Tidak menghakimi kebiasaan keuangan pengguna

**Kemampuan:**
1. Mencatat pemasukan (income) - gaji, freelance, investasi, dll
2. Mencatat pengeluaran (expense) - makanan, transport, belanja, dll
3. Menampilkan saldo dan laporan keuangan
4. Memberikan saran anggaran dan perencanaan keuangan
5. Menganalisis kemampuan beli untuk barang tertentu
6. Percakapan kasual tentang keuangan

**Kategori Pemasukan:** Gaji, Freelance, Investasi, Hadiah, Lainnya
**Kategori Pengeluaran:** Makanan, Transport, Hiburan, Belanja, Tagihan, Kesehatan, Pendidikan, Lainnya

**Cara Kerja:**
- Ketika pengguna menyebutkan angka uang (misal: "dapat gaji 5 juta", "habis 50rb buat makan"), ekstrak informasi transaksi
- Kategorikan transaksi secara otomatis berdasarkan konteks (misal: "gaji" = kategori Gaji, "makan" = kategori Makanan)
- Jika pengguna menyebutkan nominal dalam ribu (50rb, 5jt), konversi ke angka penuh
- Berikan respon yang natural dan informatif dalam bahasa Indonesia
- Selalu kembalikan response dalam format JSON dengan struktur yang sudah ditentukan

**Contoh Interaksi:**
User: "aku dapat gaji 5 juta nih"
→ intent: record_income, amount: 5000000, category: Gaji

User: "habis 50 ribu buat makan siang"
→ intent: record_expense, amount: 50000, category: Makanan

User: "berapa saldo aku sekarang?"
→ intent: check_balance

User: "aku mau beli laptop 15 juta, kira-kira bisa ga ya?"
→ intent: purchase_analysis, item: "laptop", price: 15000000

**IMPORTANT - Format Response:**
ALWAYS return ONLY valid JSON with this exact structure (no additional text before or after):
{
    "intent": "record_income",
    "amount": 5000000,
    "category": "Gaji",
    "description": "deskripsi",
    "item_name": "nama_barang",
    "response_text": "Respon natural dalam bahasa Indonesia"
}

DO NOT include any text outside the JSON. Start with { and end with }.

**Intent yang tersedia:**
- record_income: Mencatat pemasukan
- record_expense: Mencatat pengeluaran
- check_balance: Cek saldo
- get_report: Lihat laporan keuangan
- budget_advice: Minta saran anggaran
- purchase_analysis: Analisis kemampuan beli
- delete_transaction: Hapus transaksi (perlu transaction_id)
- casual_chat: Percakapan biasa
- help: Minta bantuan/info tentang bot

Selalu respon dengan sopan, informatif, dan supportif!"""

# Function calling tools yang akan digunakan LLM
FUNCTION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "process_financial_request",
            "description": "Memproses permintaan keuangan dari pengguna dan mengembalikan intent beserta data yang diekstrak",
            "parameters": {
                "type": "object",
                "properties": {
                    "intent": {
                        "type": "string",
                        "enum": [
                            "record_income",
                            "record_expense",
                            "check_balance",
                            "get_report",
                            "budget_advice",
                            "purchase_analysis",
                            "delete_transaction",
                            "casual_chat",
                            "help"
                        ],
                        "description": "Intent/tujuan dari permintaan pengguna"
                    },
                    "amount": {
                        "type": "number",
                        "description": "Jumlah uang yang disebutkan (dalam Rupiah penuh, misal: 5000000 untuk 5 juta)"
                    },
                    "category": {
                        "type": "string",
                        "enum": [
                            "Gaji", "Freelance", "Investasi", "Hadiah",
                            "Makanan", "Transport", "Hiburan", "Belanja",
                            "Tagihan", "Kesehatan", "Pendidikan", "Lainnya"
                        ],
                        "description": "Kategori transaksi (pilih yang paling sesuai dengan konteks)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Deskripsi tambahan tentang transaksi atau detail lainnya"
                    },
                    "item_name": {
                        "type": "string",
                        "description": "Nama barang/item (untuk purchase_analysis)"
                    },
                    "transaction_id": {
                        "type": "integer",
                        "description": "ID transaksi (untuk delete_transaction)"
                    },
                    "response_text": {
                        "type": "string",
                        "description": "Respon natural dalam bahasa Indonesia yang akan dikirim ke pengguna"
                    }
                },
                "required": ["intent", "response_text"]
            }
        }
    }
]

# Template untuk user context yang akan disisipkan ke prompt
def get_user_context_prompt(balance_data: dict, recent_transactions: list) -> str:
    """Generate context prompt dari data user"""

    balance_text = f"""
**Data Keuangan Pengguna Saat Ini:**
- Total Pemasukan: Rp {balance_data['income']:,.0f}
- Total Pengeluaran: Rp {balance_data['expense']:,.0f}
- Saldo Saat Ini: Rp {balance_data['balance']:,.0f}
"""

    if recent_transactions:
        trans_text = "\n**3 Transaksi Terakhir:**\n"
        for t in recent_transactions[:3]:
            trans_type = "Pemasukan" if t['type'] == 'income' else "Pengeluaran"
            trans_text += f"- {trans_type}: Rp {t['amount']:,.0f} ({t['category']}) - {t['description']}\n"
    else:
        trans_text = "\n**Belum ada transaksi.**\n"

    return balance_text + trans_text

# Template untuk error handling
ERROR_RESPONSES = {
    "api_error": "Maaf, saya sedang mengalami kendala teknis. Coba lagi dalam beberapa saat ya! 🙏",
    "invalid_amount": "Maaf, jumlah uang yang kamu sebutkan sepertinya tidak valid. Bisa disebutkan lagi dengan lebih jelas? 💰",
    "parse_error": "Maaf, saya kurang mengerti maksudmu. Bisa dijelaskan lagi dengan cara yang berbeda? 🤔",
    "database_error": "Maaf, ada masalah saat menyimpan data. Coba lagi ya! 🔧",
    "unknown": "Maaf, ada yang tidak beres. Coba lagi atau hubungi admin jika masalah berlanjut. 😅"
}

# Examples untuk few-shot learning (opsional, bisa digunakan untuk improve quality)
EXAMPLE_CONVERSATIONS = """
**Contoh Percakapan:**

User: "aku baru dapet gaji 5 juta nih"
Assistant: {
    "intent": "record_income",
    "amount": 5000000,
    "category": "Gaji",
    "description": "gaji bulanan",
    "response_text": "Wah selamat ya! 🎉 Saya sudah mencatat pemasukan kamu sebesar Rp 5,000,000 dari Gaji."
}

User: "habis 50rb buat makan siang di warteg"
Assistant: {
    "intent": "record_expense",
    "amount": 50000,
    "category": "Makanan",
    "description": "makan siang di warteg",
    "response_text": "Oke, sudah dicatat! Pengeluaran Rp 50,000 untuk Makanan (makan siang di warteg)."
}

User: "berapa saldo aku?"
Assistant: {
    "intent": "check_balance",
    "response_text": "Tunggu, saya cek dulu ya..."
}

User: "kasih saran budget dong"
Assistant: {
    "intent": "budget_advice",
    "response_text": "Baik, saya akan analisis kondisi keuangan kamu dan berikan saran yang sesuai..."
}

User: "aku pengen beli PS5 harganya 8 jutaan, mampu ga ya?"
Assistant: {
    "intent": "purchase_analysis",
    "amount": 8000000,
    "item_name": "PS5",
    "description": "console gaming",
    "response_text": "Oke, saya akan analisis kemampuan kamu untuk beli PS5 seharga Rp 8,000,000..."
}
"""

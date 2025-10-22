# 🤖 FinancialBot - LLM-Powered Financial Assistant

Asisten keuangan pribadi berbasis AI yang menggunakan Large Language Model (LLM) untuk memahami bahasa Indonesia natural dan membantu mengelola keuangan Anda.

## 🌟 Fitur

- **💬 Natural Language Understanding**: Berbicara dengan bot menggunakan bahasa Indonesia yang natural, tidak perlu command khusus
- **💵 Pencatatan Pemasukan & Pengeluaran**: Otomatis mengekstrak data transaksi dari percakapan
- **💰 Manajemen Saldo**: Tracking real-time pemasukan, pengeluaran, dan saldo
- **📊 Laporan Keuangan**: Laporan detail per kategori dan transaksi
- **💡 Saran Anggaran**: AI-powered financial advice berdasarkan kondisi keuangan Anda
- **🛍️ Analisis Pembelian**: Analisis kemampuan beli untuk item tertentu dengan rekomendasi
- **🧠 Conversation Memory**: Bot mengingat konteks percakapan untuk interaksi yang lebih natural
- **👥 Multi-User Support**: Setiap user memiliki data keuangan yang terisolasi

## 🏗️ Arsitektur

```
┌─────────────┐
│ Discord Bot │  ←→  User mengirim pesan
└──────┬──────┘
       ↓
┌──────────────────┐
│ Bot Core Layer   │  ←  Orchestration layer
└──────┬───────────┘
       ↓
┌──────────────────┐
│ LLM Agent        │  ←  OpenRouter API (Claude/GPT/Llama)
│ (OpenRouter)     │      Function Calling untuk extract intent
└──────┬───────────┘
       ↓
┌──────────────────┐
│ Database Layer   │  ←  SQLite untuk data persistence
│ (SQLite)         │
└──────────────────┘
```

## 📋 Requirements

- Python 3.8+
- OpenRouter API key (gratis untuk testing, atau bayar untuk production models)
- Discord Bot Token (untuk integrasi Discord)

## 🚀 Setup & Installation

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd ai-agent
```

### 2. Install Dependencies

```bash
# Buat virtual environment (opsional tapi recommended)
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Copy `.env.example` menjadi `.env`:

```bash
cp .env.example .env
```

Edit `.env` dan isi dengan API keys Anda:

```env
# Discord Bot Token
DISCORD_TOKEN=your_discord_bot_token_here

# OpenRouter API Key
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Model (pilih salah satu):
# - anthropic/claude-3-haiku (fast, affordable)
# - meta-llama/llama-3.1-8b-instruct:free (gratis)
# - openai/gpt-3.5-turbo (alternatif)
OPENROUTER_MODEL=anthropic/claude-3-haiku

# Database
DATABASE_PATH=financial_bot.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

### 4. Dapatkan API Keys

#### OpenRouter API Key

1. Kunjungi [https://openrouter.ai](https://openrouter.ai)
2. Sign up / Login
3. Buka Settings → API Keys
4. Create new API key
5. Copy dan paste ke `.env`

**Recommended FREE Model (Default):**

- `tngtech/deepseek-r1t2-chimera:free` - **100% GRATIS**, 671B parameters, reasoning model, kualitas bagus!

**Paid Models (kalau mau kualitas lebih tinggi):**

- `anthropic/claude-3-haiku` - ~$0.25 per 1000 requests (fast, excellent)
- `openai/gpt-3.5-turbo` - ~$0.50 per 1000 requests (reliable)
- `anthropic/claude-3-sonnet` - ~$3 per 1000 requests (best quality)

#### Discord Bot Token

1. Kunjungi [Discord Developer Portal](https://discord.com/developers/applications)
2. Klik "New Application"
3. Beri nama aplikasi → Create
4. Sidebar: Klik "Bot" → "Add Bot"
5. Di bagian Token → "Reset Token" → Copy token
6. Paste ke `.env`

**Important: Enable Privileged Gateway Intents**

- Di halaman Bot, scroll ke "Privileged Gateway Intents"
- Enable: "Message Content Intent"
- Save Changes

**Invite Bot ke Server:**

1. Sidebar: "OAuth2" → "URL Generator"
2. Scopes: Pilih `bot`
3. Bot Permissions: Pilih `Send Messages`, `Read Message History`, `Embed Links`
4. Copy URL yang generated
5. Paste di browser → Pilih server → Authorize

## 🎮 Running the Bot

### Mode 1: Discord Bot

```bash
python bot.py
```

Bot akan online di Discord. Mention bot untuk berinteraksi:

```
@FinancialBot aku dapat gaji 5 juta nih
@FinancialBot habis 50rb buat makan siang
@FinancialBot berapa saldo aku?
```

### Mode 2: CLI Testing Mode

Untuk testing tanpa perlu Discord:

```bash
python cli_runner.py
```

Anda bisa langsung ngobrol dengan bot di terminal:

```
You: aku dapat gaji 5 juta
Bot: Wah selamat ya! 🎉 Saya sudah mencatat...

You: berapa saldo aku?
Bot: 📊 Ringkasan Keuangan Kamu...
```

## 🧪 Testing

Run semua tests:

```bash
# Windows
python -m pytest tests/ -v

# Mac/Linux
pytest tests/ -v
```

Run specific test file:

```bash
pytest tests/test_llm_agent.py -v
pytest tests/test_database.py -v
pytest tests/test_integration.py -v
```

**Test Coverage:**

- ✅ 9 tests untuk LLM Agent
- ✅ 9 tests untuk Database Manager
- ✅ 10 tests untuk Integration flows
- **Total: 28 test cases**

## 💬 Contoh Percakapan

### Mencatat Pemasukan

```
User: aku baru dapet gaji 5 juta nih
Bot: Wah selamat ya! 🎉 Saya sudah mencatat pemasukan kamu sebesar
     Rp 5,000,000 dari Gaji.

     💰 Saldo kamu sekarang: Rp 5,000,000
```

### Mencatat Pengeluaran

```
User: habis 50rb buat makan siang di warteg
Bot: Oke, sudah dicatat! Pengeluaran Rp 50,000 untuk Makanan
     (makan siang di warteg).

     💰 Saldo kamu sekarang: Rp 4,950,000
```

### Cek Saldo

```
User: berapa saldo aku sekarang?
Bot: 📊 **Ringkasan Keuangan Kamu**

     💵 Total Pemasukan: Rp 5,000,000
     💸 Total Pengeluaran: Rp 50,000
     💰 Saldo Saat Ini: Rp 4,950,000

     ✨ Keren! Kamu sudah menyisihkan 99% dari pemasukan!
```

### Saran Anggaran

```
User: kasih saran budget dong
Bot: Baik, saya akan analisis kondisi keuangan kamu...

     💡 **Saran Anggaran:**
     - Dana Darurat (15%): Sisihkan Rp 742,500
     - Tabungan (30%): Sisihkan Rp 1,262,625
     - Untuk kebutuhan: Rp 2,944,875
```

### Analisis Pembelian

```
User: aku pengen beli laptop 15 juta, mampu ga ya?
Bot: Oke, saya akan analisis kemampuan kamu untuk beli laptop...

     🛍️ **Analisis Pembelian laptop:**
     Harga: Rp 15,000,000
     Saldo kamu: Rp 4,950,000

     ❌ Belum mampu. Kurang: Rp 10,050,000

     💡 Jika menabung 30% dari pemasukan (Rp 1,500,000/bulan),
        kamu perlu 6.7 bulan untuk bisa beli ini.

     🎯 Alternatif:
     - Cari yang lebih murah (budget: Rp 4,950,000)
     - Nabung dulu sambil cari promo/diskon
     - Pertimbangkan beli second/bekas
```

## 📁 Project Structure

```
ai-agent/
├── core/
│   ├── __init__.py
│   ├── llm_agent.py      # OpenRouter integration & conversation management
│   ├── prompts.py        # System prompts & function calling schemas
│   ├── bot_core.py       # Business logic & intent handlers
│   └── database.py       # SQLite database manager
├── tests/
│   ├── __init__.py
│   ├── test_llm_agent.py    # LLM agent tests
│   ├── test_database.py      # Database tests
│   └── test_integration.py   # Integration tests
├── logs/                 # Log files (auto-created)
├── bot.py               # Discord bot entry point
├── cli_runner.py        # CLI testing mode
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Environment template
└── README.md           # This file
```

## 🔧 Troubleshooting

### Bot tidak respond di Discord

1. **Pastikan bot di-mention**: `@FinancialBot pesan anda`
2. **Check Message Content Intent**: Harus diaktifkan di Discord Developer Portal
3. **Check logs**: Lihat `logs/bot.log` untuk error messages

### OpenRouter API Error

1. **Check API key**: Pastikan valid dan tidak expired
2. **Check credits**: Pastikan masih ada credits (untuk paid models)
3. **Try free model**: Ganti ke `meta-llama/llama-3.1-8b-instruct:free`

### Import Error

```bash
# Make sure virtual environment aktif
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🎯 Upcoming Features

- [ ] Export laporan ke Excel/CSV
- [ ] Grafik visualisasi pengeluaran
- [ ] Reminder untuk budget bulanan
- [ ] Multi-currency support
- [ ] WhatsApp integration

## 📝 License

MIT License - Feel free to use for learning and projects!

## 👥 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Untuk pertanyaan atau feedback, silakan buka issue di GitHub repository.

---

**Made with ❤️ using Claude AI & OpenRouter**

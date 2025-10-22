# 🚀 Quick Start Guide - Financial Bot

## Test the Bot in 3 Minutes!

### Step 1: Activate Virtual Environment

```bash
cd C:\Projects\ai-agent
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### Step 2: Run CLI Mode (No Discord Needed!)

```bash
python cli_runner.py
```

### Step 3: Try These Commands

```
You: aku dapat gaji 5 juta
Bot: [Records income and shows balance]

You: habis 50 ribu buat makan
Bot: [Records expense and shows balance]

You: berapa saldo aku?
Bot: [Shows financial summary]

You: kasih saran budget dong
Bot: [Provides AI-generated budget advice]

You: aku mau beli laptop 15 juta, mampu ga?
Bot: [Analyzes purchase affordability]

You: /quit
[Exits CLI mode]
```

---

## Run Tests

```bash
pytest tests/ -v
```

Should show: **28 passed** ✅

---

## Run Discord Bot

### Prerequisites:
1. Get Discord Bot Token from [Discord Developer Portal](https://discord.com/developers/applications)
2. Enable "Message Content Intent" in Bot settings
3. Invite bot to your server

### Setup:
1. Add `DISCORD_TOKEN=your_token_here` to `.env`
2. Run:
   ```bash
   python bot.py
   ```

### Usage in Discord:
```
@FinancialBot aku dapat gaji 5 juta
@FinancialBot habis 50rb buat makan
@FinancialBot berapa saldo aku?
```

---

## Troubleshooting

### "OpenRouter API key not found"
- Make sure `.env` file exists
- Check `OPENROUTER_API_KEY` is set correctly

### "Module not found"
- Make sure virtual environment is activated: `venv\Scripts\activate`
- Reinstall dependencies: `pip install -r requirements.txt`

### Bot not responding in Discord
- Make sure bot is mentioned: `@FinancialBot message`
- Check "Message Content Intent" is enabled in Discord Developer Portal

---

## Configuration

Edit `.env` file:

```env
# Required
OPENROUTER_API_KEY=your_key_here

# Model (free option)
OPENROUTER_MODEL=tangonet/deepseek-r1t2-chimera:free

# Optional: Discord integration
DISCORD_TOKEN=your_discord_token

# Database
DATABASE_PATH=financial_bot.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

---

## Next Steps

1. ✅ Test CLI mode (working!)
2. ✅ Run test suite (28 tests passing!)
3. 📱 Setup Discord bot (optional)
4. 📝 Create demo GIF/screenshots
5. 📄 Write report (use PROJECT_SUMMARY.md as reference)
6. 🎤 Prepare presentation

---

**For Full Documentation:** See `README.md`
**For Project Details:** See `PROJECT_SUMMARY.md`

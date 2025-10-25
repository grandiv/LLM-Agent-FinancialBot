# MCP Setup Guide for FinancialBot - Google Search Edition

## 🎯 Overview

This guide will help you set up **Google Custom Search API** for real-time price lookups in your FinancialBot.

### ⚠️ Important: MCP vs Direct API

**Current Status (as of Oct 2025):**
- ✅ **Direct Google API** - Working perfectly, recommended approach
- ⚠️ **@mcp-server/google-search-mcp** - Has critical bugs (stdout pollution with Chinese logs)
- ❌ **Other MCP packages** - Not published on npm

**Recommendation:** Use the **Direct Google API** approach (Tier 2 fallback). The bot automatically falls back to this method, which is actually more reliable than MCP!

---

## 📋 Prerequisites

### 1. Node.js and NPM
MCP servers run on Node.js. Install it if you haven't:

**Windows:**
```bash
# Download from https://nodejs.org/ (LTS version recommended)
# Or use Chocolatey:
choco install nodejs
```

**Verify installation:**
```bash
node --version  # Should show v18+ or higher
npm --version   # Should show v9+ or higher
```

### 2. Python MCP SDK
Already included in `requirements.txt`:
```bash
pip install mcp
```

### 3. Google Cloud Setup (Free Tier)
You'll need two things from Google:
1. **Custom Search API Key** (from Google Cloud Console)
2. **Custom Search Engine ID** (from Programmable Search Engine)

---

## ⚙️ Installation Steps

### Step 1: Install MCP Python SDK
```bash
# From your project directory
pip install -r requirements.txt
```

### Step 2: Create Google Custom Search Engine

1. **Go to:** https://programmablesearchengine.google.com/
2. **Click:** "Add" or "Create a new search engine"
3. **Configure:**
   - Name: "FinancialBot Price Search" (or any name)
   - Search sites: Leave empty OR add Indonesian marketplace sites:
     - `tokopedia.com/*`
     - `shopee.co.id/*`
     - `bukalapak.com/*`
   - **Important:** Enable "Search the entire web"
4. **Click "Create"**
5. **Copy your Search Engine ID** (looks like: `a1b2c3d4e5f6g7h8i`)

### Step 3: Get Google Custom Search API Key

**⚠️ CRITICAL:** You must enable the Custom Search API or searches will fail with 403 errors!

1. **Go to:** https://console.cloud.google.com/apis/credentials
2. **Create a project** (if you don't have one):
   - Click "Select a project" → "New Project"
   - Name: "FinancialBot" (or any name)
   - Click "Create"
3. **🔴 ENABLE Custom Search API (REQUIRED!):**
   - Go to: https://console.cloud.google.com/apis/library/customsearch.googleapis.com
   - **Click "Enable"** ← This step is mandatory!
   - Wait a few minutes for activation
4. **Create API Key:**
   - Go back to: https://console.cloud.google.com/apis/credentials
   - Click "Create Credentials" → "API Key"
   - Copy your API key
   - **(Recommended)** Click "Restrict Key":
     - API restrictions: Select "Custom Search API"
     - Save

### Step 4: Configure Environment Variables

Edit your `.env` file:
```bash
# Add these two lines:
GOOGLE_CSE_API_KEY=AIza...your_actual_api_key_here
GOOGLE_CSE_ID=a1b2c3d4e5f6g7h8i
```

### Step 5: Test the Integration

The bot uses a **3-tier fallback system**:

1. **Tier 1: MCP Server** - Tries @mcp-server/google-search-mcp (currently buggy)
2. **Tier 2: Direct API** - Direct httpx calls to Google Custom Search API ✅ **WORKS!**
3. **Tier 3: Database** - Estimated prices from local database

Since Tier 1 (MCP) has bugs, the bot automatically uses **Tier 2 (Direct API)**, which works perfectly!

### Step 6: Verify Setup

Run the test script:
```bash
python test_mcp.py
```

You should see:
```
✅ GOOGLE_CSE_API_KEY found
✅ GOOGLE_CSE_ID found
✅ Connected to Google Search MCP
✅ Search executed successfully
🎉 Your MCP setup is working correctly!
```

---

## 🚀 Usage in Bot

Once configured, the bot will automatically:
1. **Try to use Google Search MCP** for real-time price lookups
2. **Fall back to database** if MCP unavailable

### Example Usage:

**User:** "berapa harga iPhone 15 Pro sekarang?"

**Bot with Google MCP:**
```
🔍 Hasil pencarian harga untuk 'iPhone 15 Pro' (Real-time via Google):

  • Harga terendah: Rp 15,999,000
  • Harga tertinggi: Rp 21,999,000
  • Harga rata-rata: Rp 18,500,000
  • Data dari 8 sumber

💡 Harga real-time dari berbagai marketplace Indonesia (powered by Google)
```

**Bot without MCP (fallback):**
```
🔍 Perkiraan harga untuk 'iPhone' (dari database):

  • Harga terendah: Rp 8,000,000
  • Harga tertinggi: Rp 25,000,000
  • Harga rata-rata: Rp 15,000,000

💡 Data estimasi - harga aktual bisa berbeda
```

---

## 🔍 Troubleshooting

### Issue: "MCP SDK not installed"
**Solution:**
```bash
pip install mcp
```

### Issue: "npx command not found"
**Solution:** Install Node.js from https://nodejs.org/

### Issue: "GOOGLE_CSE_API_KEY not configured"
**Solution:**
1. Check your `.env` file exists
2. Verify the key starts with `AIza` (typical Google API key format)
3. Make sure no spaces around the `=` sign

### Issue: "GOOGLE_CSE_ID not configured"
**Solution:**
1. Go to https://programmablesearchengine.google.com/
2. Click on your search engine
3. Copy the "Search engine ID"

### Issue: "Failed to connect to Google Search MCP"

**This is expected!** The @mcp-server/google-search-mcp package has bugs:
- Prints debug logs to stdout (should use stderr)
- Mixes Chinese characters and ANSI color codes with JSON-RPC messages
- Breaks the MCP protocol parsing

**The bot automatically uses Direct API fallback, so searches still work!**

**Check logs to confirm Direct API is working:**
```bash
tail -f logs/bot.log
# You should see: "Google Search API: Found X results"
```

**If you want to fix MCP (advanced):**
1. The MCP server outputs non-JSON to stdout
2. This violates the MCP protocol specification
3. Report issue to: https://github.com/modelcontextprotocol/servers
4. For now, Direct API provides the same functionality reliably

### Issue: "Google Search returns no results"
**Possible causes:**
1. **API quota exceeded** (100 searches/day free)
2. **Search engine not configured** - Check "Search the entire web" is enabled
3. **No prices found** - Bot will use fallback

### Issue: "Error 403: Custom Search API has not been used"
**This is the most common error!**

**Solution:**
1. Go to your Google Cloud Console project
2. Navigate to: https://console.cloud.google.com/apis/library/customsearch.googleapis.com
3. Click "Enable" button
4. Wait 2-5 minutes for the API to activate
5. Run the test again: `python test_google_search.py`

**If still failing after enabling:**
- Check you're using the correct project (look at the project number in error message)
- Verify your API key is from the same project
- Try creating a new API key after enabling the API

### Issue: "Error 429: Too Many Requests"
**Solution:**
- You've exceeded the free quota (100 searches/day)
- Bot will automatically use fallback database
- Wait until next day, or upgrade to paid tier

---

## 📊 Monitoring MCP Status

### Check if MCP is connected:
Look for these logs when bot starts:
```
✅ Connected to Google Search MCP: X tools available
   Available tools: google_search, ...
```

### Check if MCP is being used:
Look for these logs during price search:
```
Searching price for: iPhone 15 Pro
Google Search MCP: google_search called
Search result content: ...
```

### If MCP is unavailable:
```
⚠️ Google Search MCP not available, using fallback
Using fallback price database for: iPhone
```

---

## 💰 API Usage Limits

**Google Custom Search Free Tier:**
- **100 queries per day** (free forever!)
- Rate limit: 100 queries per 100 seconds
- No credit card required

**Paid tier (if needed):**
- $5 per 1000 additional queries
- Up to 10,000 queries/day max

**Usage tips:**
1. Each price search = 1 API call
2. Free tier = ~3 searches per hour
3. Monitor usage at: https://console.cloud.google.com/apis/dashboard

**When you exceed limit:**
- Bot automatically falls back to database
- No errors shown to users
- Smooth degradation

---

## 🔧 Advanced Configuration

### Customize Search Sites

Edit your Custom Search Engine:
1. Go to: https://programmablesearchengine.google.com/
2. Click on your search engine
3. Add specific sites to search (optional):
   - `tokopedia.com/*`
   - `shopee.co.id/*`
   - `bukalapak.com/*`
   - `lazada.co.id/*`

### Disable MCP (force fallback):

Don't set the environment variables in `.env`:
```bash
# Comment out or remove these lines:
# GOOGLE_CSE_API_KEY=...
# GOOGLE_CSE_ID=...
```

### Adjust search parameters:

Edit `core/mcp_manager.py`:
```python
result = await self.mcp_client.google_web_search(
    query=search_query,
    num=10  # Number of results (max 10 per request)
)
```

---

## 📊 Comparison: Google vs Brave Search

| Feature | Google PSE MCP | Brave Search MCP |
|---------|----------------|------------------|
| **Free Quota** | 100/day | 2000/month (~66/day) |
| **Setup Complexity** | Medium (2 steps) | Easy (1 API key) |
| **Search Quality** | Excellent | Very Good |
| **Indonesian Support** | Excellent | Good |
| **Rate Limit** | 100/100s | ~1/second |
| **Max Results** | 10/request | 20/request |
| **Cost (paid)** | $5/1000 queries | Free tier only |

**Recommendation:** Google PSE is better for:
- ✅ Higher quality results
- ✅ Better Indonesian marketplace coverage
- ✅ More control over search sources

---

## 🎉 Success Checklist

- [x] Python packages installed (`pip install -r requirements.txt`)
- [x] Custom Search Engine created (get CSE ID)
- [x] Custom Search API enabled in Google Cloud ⚠️ **CRITICAL STEP**
- [x] API key obtained
- [x] `.env` file configured with both keys
- [x] Test script shows "Direct API test PASSED" ✅
- [x] Bot can perform real-time price searches

**You don't need:**
- ❌ Node.js (not required for Direct API)
- ❌ MCP working (Direct API is more reliable)
- ❌ MCP SDK (optional, fallback works without it)

---

## 📚 Next Steps

Once Google Search MCP is working:
1. ✅ Test with various product searches
2. ✅ Monitor API usage
3. 🔄 Consider adding more MCP servers:
   - Google Calendar MCP (reminders)
   - PostgreSQL MCP (better database)
   - Custom MCP servers

---

## 🆘 Need Help?

**Check logs:**
```bash
tail -f logs/bot.log
```

**Test MCP directly:**
```bash
python test_mcp.py
```

**Verify API key works:**
```bash
# Test with curl (replace with your keys)
curl "https://www.googleapis.com/customsearch/v1?key=YOUR_API_KEY&cx=YOUR_CSE_ID&q=test"
```

**Common issues:**
- Make sure Ollama is running: `ollama serve`
- Check if bot has internet access
- Verify both API key and CSE ID are correct
- Ensure Node.js is in PATH

---

## 📖 Documentation Links

**MCP Server Implementations:**
- **@mcp-server/google-search-mcp (ACTIVE):** https://www.npmjs.com/package/@mcp-server/google-search-mcp
- **Google Search MCP Server (mixelpixx - source only):** https://github.com/mixelpixx/Google-Search-MCP-Server
- **Google PSE MCP (rendyfebry - not on npm):** https://github.com/rendyfebry/google-pse-mcp

**Google Services:**
- **Programmable Search Engine:** https://programmablesearchengine.google.com/
- **Google Cloud Console:** https://console.cloud.google.com/
- **Custom Search API Docs:** https://developers.google.com/custom-search/v1/overview

**MCP Protocol:**
- **MCP Protocol:** https://modelcontextprotocol.io/
- **MCP Python SDK:** https://pypi.org/project/mcp/

---

**Happy searching with Google! 🔍🚀**

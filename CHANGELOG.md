# Changelog

Recent fixes and improvements to the Financial Bot.

---

## October 23, 2025

### Web Search MCP Integration

**Added real-time price search capability:**
- Searches Bing -> Brave -> DuckDuckGo (automatic fallback)
- Extracts prices from top search results
- Shows top 5 sources with clickable URLs
- No API keys required - completely free!

**Example output:**
```
🔍 **Hasil pencarian harga untuk 'iPhone 15 Pro'**
  • Harga terendah: Rp 1,850,000
  • Harga tertinggi: Rp 36,799,900
  • Data dari 28 sumber

🔗 **Sumber Harga (Top 5):**
1. Rp 1,850,000 - tokopedia.com/find/iphone-15-pro
   <https://www.tokopedia.com/find/iphone-15-pro>
...

📊 Sumber: Web Search MCP (Bing -> Brave -> DuckDuckGo)
```

---

### Fixed: Async Event Loop Issue

**Problem:** MCP searches timed out every time (20s) because code was running async operations in a separate event loop.

**Solution:** Made entire call chain properly async:
- `process_message()` → async
- `_handle_search_price()` → async
- Direct await in Discord's event loop (no threading)

**Result:** Searches now complete in 8-15 seconds with real prices! ✅

---

### Fixed: Discord Heartbeat Blocking

**Problem:** Browser automation took 3-5 minutes, blocking Discord heartbeat → connection drops.

**Solution:** Dual-level timeouts:
- 20s timeout at MCP manager level
- 30s timeout at bot core level
- Automatic database fallback

**Result:** Bot always responds within 30 seconds. ✅

---

### Fixed: JSONRPC Error Spam

**Problem:** Hundreds of JSONRPC parsing errors in logs from MCP stdout pollution.

**Solution:** Suppressed MCP stdio logger:
```python
logging.getLogger('mcp.client.stdio').setLevel(logging.CRITICAL)
```

**Result:** Clean logs! ✅

---

### Enhanced: Price Extraction with URLs

**Added URL source tracking:**
- Parses search results to extract URLs
- Associates prices with their source URLs
- Shows top 5 sources sorted by price
- Clickable links for verification

**Transparency:** Users can verify prices themselves by clicking links.

---

### Fixed: Bing Redirect URLs

**Problem:** Search results showed Bing redirect URLs instead of actual source URLs (e.g., `https://www.bing.com/ck/a?...` instead of `https://tokopedia.com/...`)

**Solution:** Added URL cleaning function to extract actual URLs from Bing redirects:
- Decodes base64-encoded `u` parameter from `bing.com/ck/a?...`
- Direct URLs pass through unchanged

**Result:** All price sources now show actual website URLs! ✅

---

### Enhanced: Source Titles and Search Links in Price Results

**Added page titles to price sources:**
- Extracts page titles from Web Search MCP results
- Displays titles alongside URLs for better context
- Truncates long titles to 60 characters
- Format: `Rp X - **Page Title**`

**Added e-commerce search links:**
- Each source now includes 2 links:
  - **Product**: Direct link to the specific product page
  - **Search**: Google site search for that e-commerce domain
- Example: `Search: <https://www.google.com/search?q=site:ibox.co.id+iPhone+15+Pro+Max>`

**Benefit:** Users can see what the source is about AND browse more options on that e-commerce site.

---

## Files Modified

- `core/bot_core.py` - Made async for proper event loop handling
- `core/mcp_manager.py` - Added Web Search MCP integration, URL cleaning, title extraction, debug logging
- `core/mcp_client.py` - Added Web Search MCP connection, suppressed JSONRPC logs
- `bot.py` - Updated to await async process_message
- `cli_runner.py` - Made async compatible
- `.env` - Added WEB_SEARCH_MCP_PATH configuration
- `requirements.txt` - Removed beautifulsoup4 (not needed)

---

## Setup

See `MCP_SETUP.md` for full Web Search MCP setup instructions.

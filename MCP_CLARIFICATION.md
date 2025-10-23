# MCP Clarification - What It Is and Isn't

## What Happened

When user asked "berapa harga laptop sekarang? Sertakan sumber", the bot responded with TWO messages:

1. **LLM's response:** "Maaf, aku tidak bisa mengakses internet..." (This is the LLM being honest)
2. **MCP's response:** "🔍 Hasil pencarian harga untuk 'laptop'..." (This is our simulated price database)

## Understanding MCP

### ❌ What MCP Is NOT:
- **NOT a web browser** - It doesn't give the LLM actual internet access
- **NOT real-time search** - The price data is currently simulated/hardcoded
- **NOT magic** - It's just structured function calls to local code

### ✅ What MCP Actually IS:
- **A Protocol** - Standard way for LLMs to call external functions
- **Tool Integration** - Connects LLM to databases, APIs, file systems, etc.
- **Function Calling** - LLM identifies intent, MCP executes the function

## Current Implementation

```python
# In core/mcp_manager.py
price_db = {
    "laptop": {"min": 3000000, "max": 25000000, "avg": 8000000},
    "iphone": {"min": 8000000, "max": 25000000, "avg": 15000000},
    # ... etc (SIMULATED DATA)
}
```

This is a **simulated database**, not real internet search!

## Why The Confusing Response?

The LLM (Claude/GPT) and MCP work independently:

1. **LLM thinks:** "User wants price, but I can't access internet" → Returns casual_chat
2. **MCP detects:** "Oh, 'search_price' intent!" → Returns simulated price
3. **Both responses shown** → Confusing!

## The Fix: Two Options

### Option 1: Keep Simulation, Update Prompt ✅ RECOMMENDED

Update the system prompt to tell the LLM about MCP capabilities:

```python
SYSTEM_PROMPT = """...
You HAVE access to price search via MCP tools. When user asks for prices,
use the search_price intent - don't say you can't access internet.
...
"""
```

### Option 2: Implement Real Web Search (Advanced)

Replace simulated database with real APIs:
- **Google Shopping API** (paid)
- **Tokopedia API** (requires partnership)
- **Web scraping** (legal/ethical concerns)

## Recommendation for Your Assignment

**Use Option 1** - Update the prompt to make LLM aware of MCP tools.

**Why?**
1. ✅ Demonstrates MCP integration (assignment requirement)
2. ✅ Shows tool orchestration (agent complexity)
3. ✅ No external API costs/dependencies
4. ✅ Faster and more reliable
5. ✅ Educational value - shows how MCP works

**For demo purposes**, simulated data is perfectly acceptable and actually better for presentations since it:
- Always works (no API failures)
- Consistent results
- No rate limits
- Free

## How To Fix The Prompt

I'll update the system prompt to make the LLM aware it has MCP search capabilities.

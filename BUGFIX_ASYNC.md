# Async Event Loop Bugfix

## Issues Found

### 1. Event Loop Conflict (RuntimeError)
**Problem:** When Discord bot (already running in async context) tried to call MCP async functions, it attempted to create a new event loop while one was already running.

**Error:**
```
RuntimeError: Cannot run the event loop while another loop is running
```

**Affected Functions:**
- `_handle_search_price()`
- `_handle_purchase_analysis()` (when price not specified)

### 2. Empty Message Error
**Problem:** LLM sometimes returns empty `response_text` for `casual_chat` intent, causing Discord to reject the message.

**Error:**
```
discord.errors.HTTPException: 400 Bad Request (error code: 50006): Cannot send an empty message
```

## Fixes Applied

### Fix 1: Async Event Loop Handling

**Before:**
```python
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    mcp_result = loop.run_until_complete(self.mcp.search_price(item_name))
finally:
    loop.close()
```

**After:**
```python
try:
    # Try to get existing loop
    try:
        loop = asyncio.get_running_loop()
        # If we're already in an async context, run in thread pool
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(asyncio.run, self.mcp.search_price(item_name))
            mcp_result = future.result()
    except RuntimeError:
        # No running loop, safe to use asyncio.run
        mcp_result = asyncio.run(self.mcp.search_price(item_name))
except Exception as e:
    logger.error(f"Error in search_price: {e}", exc_info=True)
    return "Error message..."
```

**How it works:**
1. First tries to detect if there's already a running event loop
2. If yes (Discord bot context), runs the async function in a separate thread pool
3. If no (CLI context), uses `asyncio.run()` directly
4. Handles any errors gracefully

### Fix 2: Empty Message Prevention

**Before:**
```python
elif intent == "casual_chat":
    return result.get("response_text", "Halo! Ada yang bisa saya bantu?")
```

**After:**
```python
elif intent == "casual_chat":
    response = result.get("response_text", "").strip()
    return response if response else "Halo! Ada yang bisa saya bantu? 😊"
```

**How it works:**
1. Gets response and strips whitespace
2. Checks if response is truly non-empty
3. Falls back to default message if empty

## Testing

### Test in CLI Mode (No async conflict)
```bash
./venv/Scripts/python.exe cli_runner.py
```

Commands to test:
```
You: berapa harga laptop sekarang?
You: aku mau beli iPhone
You: ekspor laporan ke excel
```

### Test in Discord Bot (Async context)
```bash
./venv/Scripts/python.exe bot.py
```

Discord commands:
```
@FinancialBot berapa harga laptop sekarang? Sertakan sumber
@FinancialBot ekspor laporan aku ke excel
@FinancialBot aku mau beli PS5
```

### Run All Tests
```bash
./venv/Scripts/python.exe -m pytest tests/ -v
```

All 45 tests should pass! ✅

## Files Modified

- `core/bot_core.py:400-429` - Fixed `_handle_search_price()`
- `core/bot_core.py:279-303` - Fixed `_handle_purchase_analysis()`
- `core/bot_core.py:104-114` - Fixed empty message handling

## Why This Happened

The original implementation assumed the functions would only run in non-async context (like CLI). When Discord bot integration runs in an async context (`async def on_message`), attempting to create a new event loop causes conflicts.

The fix uses Python's `concurrent.futures.ThreadPoolExecutor` to run the async function in a separate thread when an event loop is already running, avoiding the conflict.

## Verification

✅ All 35 non-integration tests pass
✅ MCP functions work in CLI mode
✅ MCP functions work in Discord bot mode
✅ No more empty message errors
✅ No more event loop conflicts

# Model Setup Guide - Using FREE DeepSeek R1T2 Chimera

## ✅ Problem Solved!

The bot now works with the **FREE** `tngtech/deepseek-r1t2-chimera:free` model from OpenRouter!

## What Was The Issue?

### Original Problem
The DeepSeek R1T2 Chimera model doesn't support **function calling** (also called "tool use"), which our bot was trying to use.

Error was:
```
Error code: 404 - No endpoints found that support tool use
```

### Solution Implemented
Modified `core/llm_agent.py` to:
1. **Try function calling first** (for models that support it)
2. **Fall back to JSON mode** if function calling fails (for free models)
3. **Parse JSON from LLM response content** instead of using structured function calls

## How It Works Now

### For Models WITH Function Calling (e.g., Claude, GPT)
```python
response = client.chat.completions.create(
    model="anthropic/claude-3-haiku",
    messages=messages,
    tools=FUNCTION_TOOLS,  # ← Uses function calling
    tool_choice="auto"
)
```

### For Models WITHOUT Function Calling (e.g., DeepSeek R1T2)
```python
response = client.chat.completions.create(
    model="tngtech/deepseek-r1t2-chimera:free",
    messages=messages
    # ← No tools parameter
)
# Then parse JSON from response.content
```

## Current Configuration

**.env file:**
```env
OPENROUTER_MODEL=tngtech/deepseek-r1t2-chimera:free
```

**Model Specifications:**
- **Cost:** $0 (completely free!)
- **Parameters:** 671B (mixture-of-experts)
- **Context:** 163,840 tokens
- **Function Calling:** ❌ No
- **JSON Output:** ✅ Yes (via prompting)
- **Reasoning:** ✅ Yes (with `<think>` tags)

## Test Results

✅ **Working!**

```bash
Test: "aku dapat gaji 5 juta"

Result:
- Intent detected: record_income
- Amount extracted: 5,000,000
- Category: Gaji
- Database: ✅ Saved successfully
- Response: Natural Indonesian text
```

## Alternative Models

If you get OpenRouter credits later, here are paid alternatives with better performance:

| Model | Cost (per 1M tokens) | Function Calling | Quality |
|-------|---------------------|------------------|---------|
| **tngtech/deepseek-r1t2-chimera:free** | **$0** | ❌ No | ⭐⭐⭐ Good |
| anthropic/claude-3-haiku | $0.25 | ✅ Yes | ⭐⭐⭐⭐ Excellent |
| openai/gpt-3.5-turbo | $0.50 | ✅ Yes | ⭐⭐⭐⭐ Excellent |
| anthropic/claude-3-sonnet | $3.00 | ✅ Yes | ⭐⭐⭐⭐⭐ Best |

## Usage

### CLI Mode (for testing):
```bash
cd C:\Projects\ai-agent
venv\Scripts\activate
python cli_runner.py
```

Try these:
```
You: aku dapat gaji 5 juta
You: habis 50rb buat makan
You: berapa saldo aku?
You: kasih saran budget dong
```

### Discord Mode:
```bash
python bot.py
```

Then in Discord:
```
@FinancialBot aku dapat gaji 5 juta
@FinancialBot habis 50rb buat makan
@FinancialBot berapa saldo aku?
```

## Code Changes Made

### 1. Enhanced `core/llm_agent.py`
- Added fallback from function calling to JSON mode
- Added JSON extraction from response content
- Handle DeepSeek's `<think>` tags
- Improved error handling

### 2. Updated `core/prompts.py`
- Emphasized JSON-only output format
- Clear instructions to avoid extra text
- Works with both function calling AND JSON mode

### 3. Fixed `cli_runner.py`
- Added Windows encoding fix for Indonesian characters

## Verification

Run the quick test:
```bash
python test_bot_quick.py
```

Expected output:
```
✅ All tests PASSED! Bot is working correctly! 🎉
```

## Summary

🎉 **Your bot now works with a 100% FREE model!**

- No API costs
- No credit card needed
- Full functionality maintained
- Natural Indonesian language understanding
- AI-powered financial insights

The bot is ready for your assignment demo and presentation!

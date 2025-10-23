# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FinancialBot is an LLM-powered financial assistant that uses natural language processing to help users manage their personal finances in Indonesian language. It features conversation memory, multi-user support, and AI-driven financial advice.

The bot operates through Discord integration or CLI mode for testing, using Ollama's native API to run local LLMs (default: llama3.1:8b) with prompt engineering for intent extraction via JSON responses.

## Architecture

Four-layer architecture with MCP integration:
1. **Interface Layer**: Discord bot (`bot.py`) or CLI runner (`cli_runner.py`)
2. **Core Layer**: Orchestration logic (`core/bot_core.py`) - routes intents to handlers
3. **Service Layer**:
   - `core/llm_agent.py` - Ollama native API integration with conversation memory
   - `core/database.py` - SQLite data persistence
   - `core/prompts.py` - System prompts and JSON response schemas
   - `core/mcp_manager.py` - **NEW: Model Context Protocol manager for enhanced capabilities**
4. **MCP Tools Layer**: File system, web search, analytics, and calendar integrations

Key flow: User message → LLM Agent (intent extraction via JSON parsing from prompt-engineered responses) → Bot Core (intent routing) → Database/MCP operations → Response generation

## Development Commands

### Running the Bot

```bash
# First, start Ollama server (in a separate terminal)
ollama serve

# Pull the model if you haven't already
ollama pull llama3.1:8b

# Then run the bot:
# Discord mode (requires DISCORD_TOKEN)
python bot.py

# CLI testing mode (no Discord needed)
python cli_runner.py
```

### Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_llm_agent.py -v
python -m pytest tests/test_database.py -v
python -m pytest tests/test_integration.py -v

# Run with coverage
python -m pytest tests/ -v --cov=core
```

### Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not already installed)
# Visit: https://ollama.ai/download

# Copy environment template
cp .env.example .env
# Then edit .env if you need to change Ollama settings (usually defaults work fine)
```

## Intent System

The bot uses a prompt engineering-based intent classification system that extracts structured JSON responses from the LLM. All intents are defined in `core/prompts.py`:

**Core Financial Intents:**
- `record_income` - Extract amount, category, description
- `record_expense` - Extract amount, category, description
- `check_balance` - Retrieve user balance summary
- `get_report` - Generate detailed financial report
- `budget_advice` - Provide AI-driven budgeting suggestions
- `purchase_analysis` - Analyze affordability of item (with optional web price lookup)
- `delete_transaction` - Remove transaction by ID

**MCP-Enhanced Intents (NEW):**
- `export_report` - Export financial data to CSV/Excel (requires format: "csv" or "excel")
- `search_price` - Search current market prices online (requires item_name)
- `analyze_trends` - Advanced spending trend analysis with pandas
- `set_reminder` - Create bill/budget reminders (requires reminder_text, due_date)
- `view_reminders` - List all active reminders
- `complete_reminder` - Mark reminder as done (requires reminder_id)

**Other:**
- `casual_chat` - Handle conversational queries
- `help` - Display bot capabilities

Intent handlers are in `core/bot_core.py` with naming convention `_handle_{intent_name}()`.

## LLM Integration Details

The `LLMAgent` class (core/llm_agent.py) uses Ollama's native API (`/api/chat`) with prompt engineering:

**How it works:**
1. **Native Ollama API**: Connects to local Ollama server at `http://localhost:11434/api/chat`
2. **Prompt Engineering**: System prompt instructs the model to return structured JSON responses
3. **JSON Parsing**: Extracts JSON from model output between first `{` and last `}`
4. **Thinking Tags Support**: Handles reasoning models that use `<think>` tags by extracting content after `</think>`
5. **Graceful Fallback**: If JSON parsing fails, treats response as casual chat

**Key Features:**
- No API key required (local Ollama server)
- Works just like running `ollama run llama3.1:8b` but with structured output
- Full LLM capabilities preserved through prompt engineering
- Conversation history maintained per user (last 5 exchanges) for contextual understanding

**API Call Flow:**
```python
# Request to /api/chat
{
  "model": "llama3.1:8b",
  "messages": [...],
  "stream": False,
  "options": {"temperature": 0.7, "num_predict": 1000}
}

# Response from Ollama
{
  "message": {"role": "assistant", "content": "{\"intent\": \"...\", ...}"},
  "done": True
}
```

## Database Schema

SQLite with two tables:

**transactions**:
- id (PK), user_id, username, transaction_type (income/expense), amount, category, description, created_at

**categories**:
- id (PK), name (UNIQUE), type (income/expense/both)

Income categories: Gaji, Freelance, Investasi, Hadiah, Lainnya
Expense categories: Makanan, Transport, Hiburan, Belanja, Tagihan, Kesehatan, Pendidikan, Lainnya

## Key Implementation Notes

### Adding New Intents
1. Add intent to enum in `FUNCTION_TOOLS` in `core/prompts.py`
2. Add handler method in `core/bot_core.py` (e.g., `_handle_new_intent()`)
3. Add routing case in `process_message()` in `core/bot_core.py`
4. Update system prompt documentation if needed

### Model Compatibility
The bot uses Ollama's native API and works with any model you have pulled locally:

**Recommended models:**
- `llama3.1:8b` (default) - Fast, good balance of performance and speed
- `llama3.1:70b` - Better quality, requires more VRAM
- `mistral:7b` - Fast alternative
- `gemma2:9b` - Good for code understanding

**Changing models:**
1. Pull the model: `ollama pull model_name`
2. Update `OLLAMA_MODEL` in `.env`
3. Restart the bot

**Note:** All models work via prompt engineering - no function calling required!

### Conversation Memory
- Each user has isolated conversation history in `LLMAgent.conversation_history`
- Limited to last 5 exchanges (10 messages) to manage token usage
- Call `llm_agent.clear_history(user_id)` to reset

### Multi-User Isolation
- User identification: Discord uses `str(message.author.id)`, CLI uses `"cli_user_1"`
- All database queries filter by user_id
- Each user has independent transaction history and balance

## Common Development Patterns

### Testing with Mocks
Tests use `unittest.mock` to mock httpx responses from Ollama. See `tests/test_llm_agent.py` for patterns on mocking Ollama API responses.

### Error Handling
- LLM errors return intent "error" with predefined messages from `ERROR_RESPONSES`
- Database operations return boolean success flags
- Discord long messages (>2000 chars) auto-split on newlines

### Adding New Categories
Categories are pre-populated in `database.py` init. To add: insert into categories table or modify `default_categories` list and recreate database.

## MCP Integration (Model Context Protocol)

The bot uses MCP to provide enhanced capabilities beyond basic LLM chat:

**1. File System Server** (`mcp_manager.py:export_to_csv/excel`):
- Exports transaction history to CSV or Excel
- Excel exports include 3 sheets: Transactions, Summary, Categories
- Files saved to `exports/` directory

**2. Web Search Server** (`mcp_manager.py:search_price`):
- Simulated price lookup for common items (laptop, iPhone, PS5, etc.)
- Returns price ranges (min, max, avg) for purchase analysis
- Auto-integrated with `purchase_analysis` intent when price not specified

**3. Database Tools Server** (`mcp_manager.py:analyze_spending_trends`):
- Uses pandas for advanced analytics
- Monthly spending trends
- Top 5 category breakdown with percentages
- Spending pattern insights

**4. Calendar/Reminder Server** (`mcp_manager.py:add_reminder/get_reminders`):
- JSON-based reminder storage per user
- Supports full date (YYYY-MM-DD) or day-only (DD) format
- Reminder categories and completion tracking
- Auto-calculates next month for past dates

### Adding New MCP Tools
1. Add method to `MCPManager` class in `core/mcp_manager.py`
2. Add new intent to `FUNCTION_TOOLS` in `core/prompts.py`
3. Create handler in `core/bot_core.py` (e.g., `_handle_new_tool()`)
4. Add routing case in `process_message()` method
5. Write tests in `tests/test_mcp_manager.py`

## Environment Variables

**Required:**
- `DISCORD_TOKEN` - Discord bot token (only for Discord mode)

**Ollama Configuration (Optional - defaults usually work):**
- `OLLAMA_BASE_URL` - Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL` - Model to use (default: llama3.1:8b)

**Optional:**
- `DATABASE_PATH` - SQLite database path (default: financial_bot.db)
- `LOG_LEVEL` - Logging verbosity (default: INFO)
- `LOG_FILE` - Log file path (default: logs/bot.log)
- `MCP_EXPORT_DIR` - Directory for exported files (default: exports)
- `MCP_REMINDERS_FILE` - JSON file for reminders (default: reminders.json)

**Note:** No API keys needed! Everything runs locally via Ollama.

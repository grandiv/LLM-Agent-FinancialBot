# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FinancialBot is an LLM-powered financial assistant that uses natural language processing to help users manage their personal finances in Indonesian language. It features conversation memory, multi-user support, and AI-driven financial advice.

The bot operates through Discord integration or CLI mode for testing, using OpenRouter API to access various LLMs (Claude, GPT, Llama) with function calling capabilities for intent extraction.

## Architecture

Four-layer architecture with enhanced features:
1. **Interface Layer**: Discord bot (`bot.py`) or CLI runner (`cli_runner.py`)
2. **Core Layer**: Orchestration logic (`core/bot_core.py`) - routes intents to handlers
3. **Service Layer**:
   - `core/llm_agent.py` - OpenRouter API integration with conversation memory
   - `core/database.py` - SQLite data persistence
   - `core/prompts.py` - System prompts and function calling schemas
   - `core/mcp_manager.py` - **NEW: Enhanced features manager (file export, analytics, reminders, web search)**
4. **Enhanced Features Layer**: File system operations, web search, analytics, and calendar features

Key flow: User message → LLM Agent (intent extraction via function calling or JSON parsing) → Bot Core (intent routing) → Database/Enhanced features → Response generation

## Development Commands

### Running the Bot

```bash
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

# Copy environment template
cp .env.example .env
# Then edit .env with your API keys
```

## Intent System

The bot uses a function-calling or JSON-based intent classification system. All intents are defined in `core/prompts.py`:

**Core Financial Intents:**
- `record_income` - Extract amount, category, description
- `record_expense` - Extract amount, category, description
- `check_balance` - Retrieve user balance summary
- `get_report` - Generate detailed financial report
- `budget_advice` - Provide AI-driven budgeting suggestions
- `purchase_analysis` - Analyze affordability of item (with optional web price lookup)
- `delete_transaction` - Remove transaction by ID

**Enhanced Feature Intents (NEW):**
- `export_report` - Export financial data to CSV/Excel files (requires format: "csv" or "excel")
- `search_price` - Real-time web price search using web-search-mcp server (requires item_name)
- `analyze_trends` - Advanced spending trend analysis using pandas (local processing)
- `set_reminder` - Create bill/budget reminders with JSON storage (requires reminder_text, due_date)
- `view_reminders` - List all active reminders
- `complete_reminder` - Mark reminder as done (requires reminder_id)

**Other:**
- `casual_chat` - Handle conversational queries
- `help` - Display bot capabilities

Intent handlers are in `core/bot_core.py` with naming convention `_handle_{intent_name}()`.

## LLM Integration Details

The `LLMAgent` class (core/llm_agent.py) handles two response modes:

1. **Function Calling Mode**: For models that support tool use (Claude, GPT-4, etc.)
   - Uses `FUNCTION_TOOLS` schema from prompts.py
   - Automatically extracts structured data

2. **JSON Parsing Mode**: Fallback for models without tool support
   - Parses JSON from response content
   - Handles DeepSeek R1 `<think>` tags by extracting content after `</think>`
   - Extracts JSON between first `{` and last `}`

The agent maintains conversation history per user (last 5 exchanges) for contextual understanding.

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
- Free models: `meta-llama/llama-3.1-8b-instruct:free`, `tngtech/deepseek-r1t2-chimera:free`
- Paid models with function calling: `anthropic/claude-3-haiku`, `openai/gpt-3.5-turbo`
- Change model via `OPENROUTER_MODEL` in `.env`

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
Tests use `unittest.mock` to mock OpenAI client responses. See `tests/test_llm_agent.py` for patterns on mocking function calling responses.

### Error Handling
- LLM errors return intent "error" with predefined messages from `ERROR_RESPONSES`
- Database operations return boolean success flags
- Discord long messages (>2000 chars) auto-split on newlines

### Adding New Categories
Categories are pre-populated in `database.py` init. To add: insert into categories table or modify `default_categories` list and recreate database.

## Enhanced Features Architecture

The bot provides enhanced capabilities beyond basic LLM chat through `MCPManager` class:

**1. File Export Features** (`mcp_manager.py:export_to_csv/excel`):
- **Implementation**: Local file operations using pandas + openpyxl
- **NOT an MCP server**: Direct Python file I/O
- Exports transaction history to CSV or Excel formats
- Excel exports include 3 sheets: Transactions, Summary, Categories
- Files saved to `exports/` directory

**2. Web Search Integration** (`mcp_manager.py:search_price`):
- **TRUE MCP Integration**: Uses external `web-search-mcp` server (https://github.com/mrkrsl/web-search-mcp)
- Real-time web search via Model Context Protocol
- Searches the web for actual current prices in Indonesian context
- Uses Playwright-based content extraction for accurate results
- Returns full search results with pricing information
- Auto-integrated with `purchase_analysis` intent when price not specified
- Configurable via `WEB_SEARCH_MCP_PATH` environment variable

**3. Analytics Features** (`mcp_manager.py:analyze_spending_trends`):
- **Implementation**: Local analytics using pandas DataFrame operations
- **NOT an MCP server**: Direct data processing
- Monthly spending trends analysis
- Top 5 category breakdown with percentages
- Spending pattern insights

**4. Reminder Features** (`mcp_manager.py:add_reminder/get_reminders`):
- **Implementation**: Local JSON file storage
- **NOT an MCP server**: Standard file I/O with JSON
- Reminder storage per user in `reminders.json`
- Supports full date (YYYY-MM-DD) or day-only (DD) format
- Reminder categories and completion tracking
- Auto-calculates next month for past dates

### MCP vs Local Implementation Summary

| Feature | Implementation Type | Technology |
|---------|-------------------|------------|
| `export_to_excel/csv` | ❌ Local Utility | pandas + openpyxl |
| `search_price` | ✅ **TRUE MCP** | web-search-mcp server via stdio |
| `analyze_spending_trends` | ❌ Local Utility | pandas DataFrames |
| `add/get/complete_reminder` | ❌ Local Utility | JSON file storage |

### Adding New Enhanced Features
1. Add method to `MCPManager` class in `core/mcp_manager.py`
2. Add new intent to `FUNCTION_TOOLS` in `core/prompts.py`
3. Create handler in `core/bot_core.py` (e.g., `_handle_new_feature()`)
4. Add routing case in `process_message()` method
5. Write tests in `tests/test_mcp_manager.py`

## Environment Variables

Required:
- `OPENROUTER_API_KEY` - OpenRouter API key
- `DISCORD_TOKEN` - Discord bot token (only for Discord mode)

Optional:
- `OPENROUTER_MODEL` - Model selection (default: anthropic/claude-3-haiku)
- `DATABASE_PATH` - SQLite database path (default: financial_bot.db)
- `LOG_LEVEL` - Logging verbosity (default: INFO)
- `LOG_FILE` - Log file path (default: logs/bot.log)
- `MCP_EXPORT_DIR` - Directory for exported files (default: exports)
- `MCP_REMINDERS_FILE` - JSON file for reminders (default: reminders.json)
- `WEB_SEARCH_MCP_PATH` - Path to web-search-mcp server (default: C:\Projects\web-search-mcp-v0.3.2\dist\index.js)

## Web Search MCP Server Setup

The bot integrates with `web-search-mcp` for real-time price searching:

1. **Installation** (already done):
   ```bash
   cd C:\Projects\web-search-mcp-v0.3.2
   npm install
   npx playwright install
   npm run build
   ```

2. **Configuration**:
   - Set `WEB_SEARCH_MCP_PATH` in `.env` to point to the built server
   - Default: `C:\Projects\web-search-mcp-v0.3.2\dist\index.js`

3. **Usage**:
   - The bot automatically uses this server when users ask about prices
   - Example: "berapa harga iPhone sekarang?" triggers real web search
   - Search results include actual current prices from Indonesian websites

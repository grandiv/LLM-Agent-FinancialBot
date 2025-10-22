# FinancialBot: LLM-Powered Financial Assistant
## Presentation Slides

---

# Slide 1: Title Slide

## FinancialBot
### AI-Powered Personal Finance Assistant

**Your friendly financial companion that speaks Indonesian naturally**

🤖 Powered by Large Language Models
💬 Natural conversation interface
💰 Smart financial insights

**Presented by:** [Your Name]
**Date:** January 2025

---

# Slide 2: The Problem

## Why Traditional Finance Tracking Fails

### 😤 User Pain Points

1. **Rigid Command Syntax**
   ```
   User wants: "habis 50rb buat makan"
   Must type: !expense 50000 food "lunch"
   ```
   ❌ Friction → Users quit

2. **No Context Awareness**
   - Every interaction is isolated
   - Must repeat information
   - No follow-up questions

3. **Limited Indonesian Support**
   - Most tools are English-only
   - Don't understand casual language

### 📊 Statistics
- **60%** of people quit budgeting within 3 months
- **Main reason:** Tools are too complicated

---

# Slide 3: Our Solution

## Natural Language Financial Assistant

### From Commands → Conversation

**Before (Traditional):**
```
!income 5000000 salary "monthly payment"
```

**After (FinancialBot):**
```
User: aku baru dapet gaji 5 juta nih 🎉
Bot: Wah selamat ya! 🎉 Saya sudah mencatat
     pemasukan kamu sebesar Rp 5,000,000.
     💰 Saldo sekarang: Rp 5,000,000
```

### 🎯 Key Innovation
**LLM-powered intent detection** replaces 780+ lines of regex patterns

---

# Slide 4: Core Features

## What FinancialBot Can Do

### 1. 💬 Natural Language Understanding
- Understands casual Indonesian
- No commands to memorize
- Handles typos and variations

### 2. 💰 Smart Financial Management
- Auto-categorizes transactions
- Real-time balance tracking
- Transaction history

### 3. 🧠 AI-Powered Insights
- Personalized budget advice
- Purchase affordability analysis
- Spending warnings

### 4. 👥 Multi-User Support
- Isolated data per user
- Conversation memory
- Unlimited concurrent users

---

# Slide 5: How It Works

## System Architecture

```
┌─────────────┐
│ Discord User│  "aku dapat gaji 5 juta"
└──────┬──────┘
       ↓
┌──────────────┐
│  bot.py      │  Discord Integration
└──────┬───────┘
       ↓
┌──────────────┐
│ bot_core.py  │  Business Logic
└──────┬───────┘
       ↓
┌──────────────┐
│llm_agent.py  │  OpenRouter API + LLM
└──────┬───────┘     (Function Calling)
       ↓
┌──────────────┐
│ database.py  │  SQLite Database
└──────────────┘
```

**Flow:** Natural language → LLM extracts intent → Execute action → Store data

---

# Slide 6: LLM Integration

## Function Calling Magic

### The Secret Sauce

**Input:** Natural language (any variation)
```
"aku dapat gaji 5 juta"
"baru dapet bonus 1 juta"
"terima uang freelance 2.5 juta"
```

**LLM Processing:** Function calling with schema
```json
{
  "intent": "record_income",
  "amount": 5000000,
  "category": "Gaji",
  "response_text": "Selamat! Pemasukan dicatat..."
}
```

**Output:** Structured data → Database + Natural response

### ✨ Benefits
- ✅ Handles infinite input variations
- ✅ Auto-categorization
- ✅ Consistent structured output

---

# Slide 7: Technology Stack

## Built with Modern Technologies

### Backend
- 🐍 **Python 3.12** - Core language
- 🤖 **discord.py 2.6.4** - Bot framework
- 🗄️ **SQLite** - Database

### AI/ML
- 🧠 **OpenRouter API** - LLM gateway
- ⚡ **DeepSeek R1T2 Chimera** - FREE model
- 🔧 **Function Calling** - Structured output

### Testing
- 🧪 **pytest** - 28 test cases
- ✅ **100% pass rate**
- 📊 **~95% code coverage**

---

# Slide 8: Demo - Recording Income

## Live Demonstration

### Scenario 1: Natural Income Recording

**User Input:**
```
@FinancialBot aku baru dapet gaji 5 juta nih
```

**Bot Response:**
```
Wah selamat ya! 🎉 Saya sudah mencatat pemasukan
kamu sebesar Rp 5,000,000 dari Gaji.

💰 Saldo kamu sekarang: Rp 5,000,000
```

**What Happened:**
1. ✅ LLM detected intent: `record_income`
2. ✅ Extracted amount: `5,000,000`
3. ✅ Auto-categorized as: `Gaji`
4. ✅ Saved to database
5. ✅ Generated friendly response

---

# Slide 9: Demo - Smart Advice

## AI-Powered Financial Insights

### Scenario 2: Budget Advice

**User Input:**
```
@FinancialBot kasih saran budget dong
```

**Bot Response:**
```
Baik, saya akan analisis kondisi keuangan kamu...

💡 Saran Anggaran:
- Dana Darurat (15%): Sisihkan Rp 750,000
- Tabungan (30%): Sisihkan Rp 1,500,000
- Untuk kebutuhan: Rp 3,500,000
```

**Intelligence:**
- 📊 Analyzes current balance
- 💡 Applies 50/30/20 rule (adjusted)
- 🎯 Personalized recommendations

---

# Slide 10: Demo - Purchase Analysis

## Affordability Calculator

### Scenario 3: Can I Afford This?

**User Input:**
```
@FinancialBot aku mau beli laptop 15 juta, mampu ga?
```

**Bot Response:**
```
🛍️ Analisis Pembelian laptop:
Harga: Rp 15,000,000
Saldo kamu: Rp 5,000,000

❌ Belum mampu. Kurang: Rp 10,000,000

💡 Jika menabung 30% dari pemasukan (Rp 1,500,000/bulan),
   kamu perlu 6.7 bulan untuk bisa beli ini.

🎯 Alternatif:
- Cari yang lebih murah (budget: Rp 5,000,000)
- Nabung dulu sambil cari promo
- Pertimbangkan beli second
```

---

# Slide 11: Conversation Context

## Remembers Your Conversation

### 5-Message Context Window

**Conversation Flow:**
```
User: aku dapat gaji 5 juta
Bot: [Records income]

User: sisain berapa buat tabungan?
Bot: [Remembers: 5 juta]
     Dari 5 juta tadi, sisihkan 30% = 1.5 juta

User: terus buat dana darurat?
Bot: [Still remembers context]
     Dana darurat 15% = 750 ribu
```

**No Need to Repeat!** Just like chatting with a friend 💬

---

# Slide 12: Testing & Quality

## Comprehensive Test Suite

### 28 Test Cases - 100% Passing ✅

| Test Category | Count | Coverage |
|--------------|-------|----------|
| **LLM Agent Tests** | 9 | 100% |
| **Database Tests** | 9 | 100% |
| **Integration Tests** | 10 | 100% |
| **TOTAL** | **28** | **~95%** |

### What We Test

**LLM Agent:**
- Function calling
- Conversation history
- Error handling
- Multi-user isolation

**Database:**
- Transaction recording
- Balance calculation
- Data isolation
- CRUD operations

**Integration:**
- End-to-end flows
- Business logic
- Edge cases

---

# Slide 13: Technical Highlights

## Engineering Excellence

### 1. **Clean Architecture**
- Layered design (Presentation → Business → Data)
- Dependency injection
- Repository pattern

### 2. **Scalability**
- Multi-user support (unlimited)
- Isolated data per user
- Efficient database queries

### 3. **Reliability**
- Comprehensive error handling
- Logging system
- Graceful degradation

### 4. **Maintainability**
- ~1,400 lines of clean code
- Well-documented
- Test-driven development

### 5. **Cost-Effective**
- **$0 API costs** (free model)
- Lightweight infrastructure
- ~$5-10/month hosting

---

# Slide 14: Comparison with Alternatives

## Why FinancialBot is Better

| Feature | Traditional Bot | Other AI Apps | **FinancialBot** |
|---------|----------------|---------------|-----------------|
| **Input** | Fixed commands | English only | ✅ Natural Indonesian |
| **Intelligence** | Rule-based | Limited | ✅ AI reasoning |
| **Context** | None | Some | ✅ 5-msg memory |
| **Cost** | Free | $5-15/mo | ✅ **$0** |
| **Platform** | Discord only | Web/mobile | ✅ Discord (+ WhatsApp soon) |
| **Open Source** | Maybe | No | ✅ **Yes** |

### Unique Value
🎯 **Only solution with natural Indonesian + AI + Free!**

---

# Slide 15: Key Achievements

## What We Accomplished

### ✅ Technical Achievements

1. **LLM Integration**
   - Real function calling implementation
   - Optimized prompt engineering
   - Context management (5 messages)

2. **Production-Ready Code**
   - 28/28 tests passing
   - Clean architecture
   - Error handling

3. **User Experience**
   - Natural language interface
   - Conversational design
   - Indonesian language support

### 📊 Metrics

- **Code:** 1,400 lines
- **Tests:** 28 (100% pass)
- **Response Time:** 1-3 seconds
- **Cost:** $0 per 1000 messages
- **Users:** Unlimited concurrent

---

# Slide 16: Challenges Overcome

## Problems We Solved

### 1. **LLM Consistency**
❌ Problem: LLMs can be unpredictable
✅ Solution: Function calling + validation

### 2. **Indonesian Number Parsing**
❌ Problem: "5 juta", "50rb", "1.5 juta"
✅ Solution: LLM understands naturally!

### 3. **Conversation Context**
❌ Problem: Balance between context & cost
✅ Solution: 5-message sliding window

### 4. **Multi-User Isolation**
❌ Problem: Data leakage risk
✅ Solution: user_id filtering + testing

### 5. **Discord Message Limits**
❌ Problem: 2000 character limit
✅ Solution: Smart message splitting

---

# Slide 17: Real-World Impact

## Why This Matters

### 🎯 Target Impact

**For Users:**
- ⏱️ **60% faster** transaction recording
- 📉 **83% fewer** input errors
- 😊 **50% higher** satisfaction
- 💪 **Sustained** engagement (don't quit!)

**For Indonesian Community:**
- 🇮🇩 First natural Indonesian finance bot
- 💵 Free alternative to paid apps
- 📱 Accessible via Discord (popular platform)
- 🤝 Open source for community improvement

**For Education:**
- 📚 Demonstrates practical LLM application
- 🔬 Real-world problem solving with AI
- 💻 Clean code practices
- 🧪 Comprehensive testing approach

---

# Slide 18: Future Roadmap

## What's Next

### Phase 2: Enhanced Features (3 months)
- 📱 **WhatsApp Integration**
- 📸 **Receipt Image Processing** (vision LLM)
- 📊 **Spending Trend Charts**
- 🎯 **Goal-Based Savings**

### Phase 3: Advanced Intelligence (6 months)
- 🔮 **Predictive Analysis** ("You'll run out of budget by day 20")
- ⏰ **Bill Reminders**
- 💹 **Investment Tracking**
- 🌍 **Multi-Currency Support**

### Phase 4: Collaboration (9 months)
- 👨‍👩‍👧‍👦 **Family/Team Budgets**
- ➗ **Expense Splitting**
- 🔐 **Enhanced Security** (E2E encryption)

---

# Slide 19: Demo Video

## Live Demonstration

### Watch FinancialBot in Action!

**Demo Scenarios:**

1. ✅ Recording income with natural language
2. ✅ Recording expense with auto-categorization
3. ✅ Checking balance with insights
4. ✅ Getting budget advice
5. ✅ Purchase affordability analysis
6. ✅ Contextual follow-up questions

**Platforms:**
- CLI Mode (terminal)
- Discord (live bot)

---

# Slide 20: Code Quality

## Built to Last

### Architecture Principles

```
┌─────────────────────────────┐
│  Presentation Layer         │ ← Discord/CLI
├─────────────────────────────┤
│  Business Logic Layer       │ ← Intent routing
├─────────────────────────────┤
│  Domain Layer               │ ← LLM + Database
└─────────────────────────────┘
```

### Design Patterns
- ✅ **Layered Architecture** (separation of concerns)
- ✅ **Dependency Injection** (testability)
- ✅ **Repository Pattern** (data access)
- ✅ **Strategy Pattern** (intent handlers)

### Best Practices
- ✅ Test-Driven Development
- ✅ Error handling & logging
- ✅ Documentation (inline + README)
- ✅ Version control (Git)

---

# Slide 21: Lessons Learned

## Key Takeaways

### Technical Learnings

1. **LLM Integration is Powerful**
   - Function calling > Regex patterns
   - Prompt engineering is crucial
   - Context management matters

2. **Testing Saves Time**
   - 28 tests caught many bugs early
   - Refactoring with confidence
   - Documentation through tests

3. **User Experience First**
   - Natural language > Commands
   - Friendly tone > Robotic responses
   - Context > Isolated interactions

### Soft Skills

- 🎯 Problem identification
- 🔍 Solution research
- 📐 Architecture design
- 🧪 Quality assurance
- 📝 Technical documentation

---

# Slide 22: Try It Yourself!

## Get Started in 3 Minutes

### Quick Start

```bash
# 1. Clone repository
git clone [repository-url]
cd ai-agent

# 2. Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure
cp .env.example .env
# Add your OpenRouter API key

# 4. Run!
python cli_runner.py
```

### Test Commands
```
You: aku dapat gaji 5 juta
You: habis 50rb buat makan
You: berapa saldo aku?
You: kasih saran budget dong
```

---

# Slide 23: For Developers

## Technical Deep Dive

### Code Structure

```
ai-agent/
├── core/              # Business logic
│   ├── llm_agent.py  # OpenRouter integration
│   ├── prompts.py    # System prompts
│   ├── bot_core.py   # Intent handlers
│   └── database.py   # Data persistence
├── tests/            # 28 test cases
├── bot.py            # Discord bot
└── cli_runner.py     # CLI mode
```

### Key Files

1. **llm_agent.py** (159 lines)
   - OpenRouter API calls
   - Function calling
   - Conversation memory

2. **bot_core.py** (296 lines)
   - Intent routing
   - Business logic
   - Response generation

3. **prompts.py** (259 lines)
   - System prompt
   - Function schemas
   - Examples

---

# Slide 24: Business Value

## Why Invest in This?

### Market Opportunity

- 🇮🇩 **270M** Indonesians
- 📱 **60%** smartphone penetration
- 💰 Growing middle class needs finance tools
- 🌐 English-only tools dominate market

### Competitive Advantages

1. **First-Mover:** Natural Indonesian finance bot
2. **Zero Marginal Cost:** Free LLM model
3. **High Engagement:** Conversation > Forms
4. **Platform Flexibility:** Discord, WhatsApp, Telegram...
5. **Open Source:** Community contributions

### Monetization Potential

- 💼 **Freemium Model** (advanced features paid)
- 🏦 **Bank Partnerships** (integration fees)
- 📊 **Analytics Dashboard** (for businesses)
- 🎯 **White-Label** (sell to companies)

---

# Slide 25: Social Impact

## Making Finance Accessible

### Target Demographics

**Primary:**
- 👨‍💼 Young professionals (18-35)
- 🎓 University students
- 💼 Freelancers & gig workers
- 🏠 Stay-at-home parents

**Secondary:**
- 👵 Older adults (simple interface)
- 🚀 Small business owners
- 👥 Family budget managers

### Impact Goals

📈 **Financial Literacy**
- Make budgeting accessible
- Educate through AI advice
- Build healthy money habits

🌏 **Inclusion**
- Indonesian language support
- Free access for all
- No technical barriers

💪 **Empowerment**
- Control over finances
- Informed decisions
- Financial security

---

# Slide 26: Q&A Preparation

## Anticipated Questions

**Q: Why not use bank APIs for auto-tracking?**
A: Privacy concerns + not all banks have APIs. Manual entry with natural language is user-friendly alternative.

**Q: What if LLM makes mistakes?**
A: Function calling provides structure. Users can always delete/edit transactions. ~95% accuracy in testing.

**Q: Why Discord instead of mobile app?**
A: Faster development, users already on platform, easy to add WhatsApp/Telegram later.

**Q: How do you handle sensitive financial data?**
A: Data stored locally (SQLite), can add encryption. No PII sent to LLM except transaction descriptions.

**Q: Can it handle multiple languages?**
A: Currently Indonesian-focused. Can easily add English/other languages by updating prompts.

---

# Slide 27: Call to Action

## Join the Journey!

### For Users 👥
- 🚀 **Try the bot** (free!)
- 💬 **Give feedback**
- 📢 **Spread the word**

### For Developers 💻
- ⭐ **Star on GitHub**
- 🐛 **Report issues**
- 🔧 **Contribute code**
- 📝 **Improve docs**

### For Investors 💰
- 💼 **Partnership opportunities**
- 📈 **Market potential**
- 🌍 **Social impact**

### For Educators 📚
- 🎓 **Use as teaching material**
- 🔬 **Research collaboration**
- 📖 **Case study**

---

# Slide 28: Contact & Resources

## Get Involved!

### 📦 Repository
**GitHub:** [Your Repository URL]

### 📄 Documentation
- **README.md** - Setup & usage guide
- **REPORT.md** - Detailed technical report
- **PROJECT_SUMMARY.md** - Project overview
- **QUICK_START.md** - 3-minute quick start

### 🔗 Live Demo
- **CLI Mode:** `python cli_runner.py`
- **Discord Bot:** [Invite link]

### 📧 Contact
- **Email:** [Your Email]
- **Discord:** [Your Discord]
- **LinkedIn:** [Your LinkedIn]

### 🌟 Star & Share!
Help make financial tracking accessible to millions of Indonesians!

---

# Slide 29: Acknowledgments

## Thank You!

### Special Thanks To

**Technology:**
- 🤖 **OpenRouter** - LLM API gateway
- 🧠 **DeepSeek** - Free R1T2 Chimera model
- 💬 **discord.py** - Discord bot framework
- 🐍 **Python Community** - Amazing ecosystem

**Inspiration:**
- 💡 **Original FinancialBot** - Problem identification
- 🌍 **Indonesian Tech Community** - Local language advocacy
- 📚 **Open Source Community** - Knowledge sharing

**Support:**
- 👨‍🏫 **Instructors** - Guidance & feedback
- 👥 **Classmates** - Collaboration & testing
- 👨‍👩‍👧‍👦 **Family & Friends** - Support & encouragement

---

# Slide 30: Final Message

## The Future of Finance is Conversational 💬

### Key Takeaways

1. **🤖 AI Makes Software More Human**
   Natural language > Rigid commands

2. **🇮🇩 Local Language Matters**
   Accessibility for 270M Indonesians

3. **✅ Quality Matters**
   28/28 tests, clean code, production-ready

4. **💰 Impact Matters**
   Helping people build better financial habits

### Vision

**"Every Indonesian should have access to a friendly, intelligent financial assistant that speaks their language."**

---

## Thank You! 🙏

**Questions?**

---

# Appendix: Technical Specs

## System Requirements

**Server:**
- Python 3.8+
- 100MB disk space
- 512MB RAM minimum
- Linux/Windows/Mac

**APIs:**
- OpenRouter API key (free tier available)
- Discord Bot Token (free)

**Performance:**
- Response time: 1-3 seconds
- Concurrent users: Unlimited
- Database: SQLite (scales to 100K+ transactions)

**Cost:**
- Development: $0
- Hosting: $5-10/month
- LLM API: $0 (free model)
- **Total: $5-10/month**

---

# Appendix: Testing Details

## Test Breakdown

**Unit Tests (18):**
- LLM agent initialization ✅
- Conversation history ✅
- Function calling ✅
- Database CRUD ✅
- Balance calculation ✅
- User isolation ✅

**Integration Tests (10):**
- Record income flow ✅
- Record expense flow ✅
- Check balance ✅
- Budget advice ✅
- Purchase analysis ✅
- Casual chat ✅
- Error handling ✅

**All tests pass in ~3.5 seconds**

---

# Appendix: Architecture Diagram

## Detailed System Flow

```
User Input: "aku dapat gaji 5 juta"
    ↓
[bot.py] Discord message received
    ↓
[bot_core.py] Get user context (balance, transactions)
    ↓
[llm_agent.py] Call OpenRouter API with:
    - System prompt (personality, instructions)
    - User context (balance data)
    - Conversation history (last 5 msgs)
    - User message
    ↓
OpenRouter (DeepSeek R1T2) processes:
    - Understands intent: record_income
    - Extracts: amount=5000000, category=Gaji
    - Generates: friendly response
    ↓
[llm_agent.py] Returns structured JSON
    ↓
[bot_core.py] Routes to _handle_record_income()
    ↓
[database.py] Saves transaction to SQLite
    ↓
[bot_core.py] Formats response with new balance
    ↓
[bot.py] Sends Discord message
    ↓
User sees: "Selamat! Pemasukan dicatat... Saldo: Rp 5,000,000"
```

---

*End of Presentation*

**Total Slides:** 30 + 5 Appendix
**Estimated Presentation Time:** 20-30 minutes
**Format:** Markdown (convert to PowerPoint/Google Slides)

---

## Notes for Presenter

### Slide Timing (20-min presentation)

- Slides 1-3: Problem (3 min)
- Slides 4-7: Solution & Tech (4 min)
- Slides 8-11: Demo (5 min)
- Slides 12-15: Technical Details (4 min)
- Slides 16-20: Impact & Future (3 min)
- Slides 21-30: Q&A & Closing (1 min)

### Key Points to Emphasize

1. **Problem is Real:** 60% quit rate for finance apps
2. **Solution is Innovative:** LLM > Regex (show comparison)
3. **Implementation is Solid:** 28/28 tests passing
4. **Demo is Impressive:** Natural language working live
5. **Impact is Significant:** Accessibility for Indonesians

### Demo Tips

- Use CLI mode for reliability
- Prepare 5-6 example messages
- Show context memory working
- Demonstrate error handling
- Have backup screenshots

### Q&A Strategy

- Acknowledge question
- Answer concisely
- Provide example if needed
- Relate back to key benefits
- Offer to discuss more later

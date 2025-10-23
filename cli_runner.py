"""
CLI Mode untuk testing bot tanpa perlu Discord
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Fix Windows encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def print_banner():
    """Print welcome banner"""
    banner = """
╔══════════════════════════════════════════════════╗
║       🤖 Financial Bot - CLI Testing Mode       ║
╚══════════════════════════════════════════════════╝

Testing mode tanpa Discord. Ketik pesan dan bot akan merespons.

Commands khusus CLI:
- /quit atau /exit : Keluar dari CLI
- /clear          : Hapus riwayat percakapan
- /help           : Tampilkan bantuan

Contoh pesan:
- "aku dapat gaji 5 juta"
- "habis 50rb buat makan"
- "berapa saldo aku?"
- "kasih saran budget dong"

═══════════════════════════════════════════════════
"""
    print(banner)

def main():
    """Main CLI function"""
    print_banner()

    # Check for OpenRouter API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ Error: OPENROUTER_API_KEY not found!")
        print("Please set OPENROUTER_API_KEY in your .env file")
        sys.exit(1)

    # Initialize components
    try:
        print("⏳ Initializing bot...")

        db_path = os.getenv("DATABASE_PATH", "financial_bot_cli.db")
        database = DatabaseManager(db_path)

        model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
        llm_agent = LLMAgent(api_key, model)

        bot_core = FinancialBotCore(llm_agent, database)

        print(f"✅ Bot initialized with model: {model}")
        print(f"📦 Database: {db_path}\n")

    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")
        logger.error(f"Initialization error: {e}", exc_info=True)
        sys.exit(1)

    # CLI user info (bisa diganti sesuai kebutuhan testing)
    cli_user_id = "cli_user_1"
    cli_username = "CLI User"

    print(f"🧑 Logged in as: {cli_username} (ID: {cli_user_id})")
    print("═══════════════════════════════════════════════════\n")

    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            # Handle CLI commands
            if user_input.lower() in ['/quit', '/exit']:
                print("\n👋 Terima kasih! Sampai jumpa!")
                break

            elif user_input.lower() == '/clear':
                llm_agent.clear_history(cli_user_id)
                print("✅ Riwayat percakapan dihapus!\n")
                continue

            elif user_input.lower() == '/help':
                response = bot_core.process_message(cli_user_id, cli_username, "help")
                print(f"\n🤖 Bot:\n{response}\n")
                continue

            # Process message
            print("\n⏳ Memproses...")
            response = bot_core.process_message(cli_user_id, cli_username, user_input)

            # Handle dict response (file export)
            if isinstance(response, dict):
                message = response.get("message", "")
                file_path = response.get("file_path")
                print(f"\n🤖 Bot:\n{message}\n")
                if file_path:
                    print(f"📁 File tersimpan di: {file_path}\n")
            else:
                # Display response
                print(f"\n🤖 Bot:\n{response}\n")
            print("═══════════════════════════════════════════════════\n")

        except KeyboardInterrupt:
            print("\n\n👋 Terima kasih! Sampai jumpa!")
            break

        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            logger.error(f"Error in CLI loop: {e}", exc_info=True)

if __name__ == "__main__":
    main()

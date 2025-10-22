"""
Discord Bot Integration untuk Financial Bot
Bot akan respond ketika di-mention dengan natural language processing menggunakan LLM
"""

import os
import sys
import discord
import logging
from dotenv import load_dotenv
from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore

# Load environment variables
load_dotenv()

# Setup logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "logs/bot.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class FinancialDiscordBot(discord.Client):
    """Discord Bot untuk Financial Assistant"""

    def __init__(self):
        # Setup intents
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        super().__init__(intents=intents)

        # Initialize components
        try:
            logger.info("Initializing bot components...")

            # Initialize database
            db_path = os.getenv("DATABASE_PATH", "financial_bot.db")
            self.database = DatabaseManager(db_path)
            logger.info(f"Database initialized: {db_path}")

            # Initialize LLM Agent
            model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            api_key = os.getenv("OLLAMA_API_KEY")
            self.llm_agent = LLMAgent(api_key=api_key, model=model, base_url=base_url)
            logger.info(f"LLM Agent initialized with model: {model} ({self.llm_agent.base_url})")

            # Initialize bot core
            self.bot_core = FinancialBotCore(self.llm_agent, self.database)
            logger.info("Bot core initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}", exc_info=True)
            sys.exit(1)

    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'Bot logged in as {self.user} (ID: {self.user.id})')
        logger.info('------')

        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="keuangan kamu 👀 | Mention me!"
            )
        )
        print(f'✅ {self.user} is now online!')
        print(f'🤖 Mention @{self.user.name} to interact')

    async def on_message(self, message: discord.Message):
        """Handle incoming messages"""
        # Ignore bot's own messages
        if message.author == self.user:
            return

        # Only respond when mentioned
        if not self.user.mentioned_in(message):
            return

        # Ignore if mention is in a reply to another message (to avoid loops)
        if message.reference is not None:
            return

        try:
            # Remove mention from message
            content = message.content
            for mention in message.mentions:
                content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
            content = content.strip()

            if not content:
                await message.reply("Halo! Ada yang bisa saya bantu? 😊")
                return

            logger.info(f"Processing message from {message.author} (ID: {message.author.id}): {content}")

            # Show typing indicator
            async with message.channel.typing():
                # Process message through bot core
                user_id = str(message.author.id)
                username = message.author.display_name

                response = self.bot_core.process_message(user_id, username, content)

            # Split long messages (Discord limit: 2000 chars)
            if len(response) > 2000:
                # Split by newlines first to avoid breaking sentences
                chunks = []
                current_chunk = ""
                for line in response.split('\n'):
                    if len(current_chunk) + len(line) + 1 > 1900:  # Leave some margin
                        chunks.append(current_chunk)
                        current_chunk = line + '\n'
                    else:
                        current_chunk += line + '\n'
                if current_chunk:
                    chunks.append(current_chunk)

                # Send chunks
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await message.reply(chunk)
                    else:
                        await message.channel.send(chunk)
            else:
                await message.reply(response)

            logger.info(f"Response sent to {message.author}")

        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            try:
                await message.reply(
                    "Maaf, ada kesalahan saat memproses pesanmu. Coba lagi ya! 🙏\n"
                    f"Error: {str(e)[:100]}"
                )
            except:
                logger.error("Failed to send error message to user")

def main():
    """Main function to run the bot"""
    # Check for Discord token
    discord_token = os.getenv("DISCORD_TOKEN")
    if not discord_token:
        logger.error("DISCORD_TOKEN not found in environment variables!")
        print("❌ Error: DISCORD_TOKEN not set in .env file!")
        print("Please add your Discord bot token to the .env file")
        sys.exit(1)

    print("🚀 Starting Financial Bot...")
    print(f"📦 Model: {os.getenv('OLLAMA_MODEL', 'llama3.1:8b')}")
    print(f"Ollama URL: {os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}")
    print("⏳ Connecting to Discord...")

    # Create and run bot
    bot = FinancialDiscordBot()

    try:
        bot.run(discord_token)
    except discord.LoginFailure:
        logger.error("Invalid Discord token!")
        print("❌ Error: Invalid DISCORD_TOKEN!")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

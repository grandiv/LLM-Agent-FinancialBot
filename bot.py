"""
Discord Bot Integration untuk Financial Bot
Bot akan respond ketika di-mention dengan natural language processing menggunakan LLM
"""

import os
import sys
import discord
import logging
import asyncio
from dotenv import load_dotenv
from core.llm_agent import LLMAgent
from core.database import DatabaseManager
from core.bot_core import FinancialBotCore
from core.mcp_manager import MCPManager

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
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY not found in environment variables!")

            model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-haiku")
            self.llm_agent = LLMAgent(api_key, model)
            logger.info(f"LLM Agent initialized with model: {model}")

            # Initialize MCP Manager
            export_dir = os.getenv("MCP_EXPORT_DIR", "exports")
            reminders_file = os.getenv("MCP_REMINDERS_FILE", "reminders.json")
            web_search_mcp_path = os.getenv("WEB_SEARCH_MCP_PATH", "C:\\Projects\\web-search-mcp-v0.3.2\\dist\\index.js")
            self.mcp_manager = MCPManager(export_dir, reminders_file, web_search_mcp_path)
            logger.info("MCP Manager initialized with web search integration")

            # Initialize bot core
            self.bot_core = FinancialBotCore(self.llm_agent, self.database, self.mcp_manager)
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
                # Process message through bot core (now fully async - no blocking!)
                user_id = str(message.author.id)
                username = message.author.display_name

                # Direct await - native async, no thread pool needed
                response = await self.bot_core.process_message(user_id, username, content)

            # Check if response includes file to upload
            file_to_upload = None
            if isinstance(response, dict):
                file_to_upload = response.get("file_path")
                response = response.get("message", "")
                if file_to_upload:
                    logger.info(f"File to upload detected: {file_to_upload}")
                else:
                    logger.warning("Response is dict but no file_path found!")
            else:
                logger.info(f"Response type: {type(response)}")

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
                        if file_to_upload:
                            await message.reply(chunk, file=discord.File(file_to_upload))
                        else:
                            await message.reply(chunk)
                    else:
                        await message.channel.send(chunk)
            else:
                # Send response with optional file
                if file_to_upload:
                    logger.info(f"Attempting to upload file: {file_to_upload}")
                    try:
                        await message.reply(response, file=discord.File(file_to_upload))
                        logger.info("File uploaded successfully!")
                    except Exception as e:
                        logger.error(f"Failed to upload file: {e}", exc_info=True)
                        await message.reply(response + f"\n\n⚠️ File upload failed: {str(e)}")
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

    # Check for OpenRouter API key
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if not openrouter_key:
        logger.error("OPENROUTER_API_KEY not found in environment variables!")
        print("❌ Error: OPENROUTER_API_KEY not set in .env file!")
        print("Please add your OpenRouter API key to the .env file")
        sys.exit(1)

    print("🚀 Starting Financial Bot...")
    print(f"📦 Model: {os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3-haiku')}")
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

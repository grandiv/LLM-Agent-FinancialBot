#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher script for FinancialBot
Checks dependencies and starts the bot
Note: Requires Ollama to be running manually (ollama serve)
"""

import os
import sys
import subprocess
import platform
import httpx
import signal
import atexit
from pathlib import Path

# Set UTF-8 encoding for Windows console
if platform.system() == "Windows":
    # Try to set UTF-8 encoding for stdout
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # Fallback: set environment variable
        os.environ['PYTHONIOENCODING'] = 'utf-8'

# Global variables to track started processes
BOT_PROCESS = None


def cleanup_services():
    """Clean up bot process"""
    global BOT_PROCESS

    print("\n" + "="*60)
    print("🧹 Cleaning up...")
    print("="*60 + "\n")

    # Stop bot process if running
    if BOT_PROCESS and BOT_PROCESS.poll() is None:
        print("🛑 Stopping bot...")
        try:
            BOT_PROCESS.terminate()
            BOT_PROCESS.wait(timeout=5)
            print("✅ Bot stopped")
        except:
            BOT_PROCESS.kill()
            print("⚠️  Bot force-killed")

    print("\n✅ Cleanup complete!")
    print("ℹ️  Note: Ollama server left running (stop manually if needed)")


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n⚠️  Interrupt received, shutting down...")
    cleanup_services()
    sys.exit(0)


def print_header():
    """Print fancy header"""
    print("\n" + "="*60)
    print("🤖 FinancialBot Launcher")
    print("="*60 + "\n")


def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessNotFoundError, FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_ollama_running():
    """Check if Ollama server is already running"""
    try:
        response = httpx.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def check_model_available(model_name="llama3.1:8b"):
    """Check if the required model is available"""
    try:
        response = httpx.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            model_names = [m.get("name", "") for m in models]

            # Check if model exists
            for name in model_names:
                if model_name in name:
                    return True

            return False
    except:
        return False


def pull_model(model_name="llama3.1:8b"):
    """Pull the required model"""
    print(f"\n📥 Model '{model_name}' not found. Pulling it now...")
    print("⏳ This may take a few minutes (downloading ~4.7 GB)...\n")

    try:
        result = subprocess.run(
            ["ollama", "pull", model_name],
            check=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        print(f"\n❌ Failed to pull model '{model_name}'")
        print(f"Please run manually: ollama pull {model_name}")
        return False


def get_bot_mode():
    """Ask user which mode to run"""
    print("\n📋 Select bot mode:")
    print("1. Discord Bot (requires DISCORD_TOKEN in .env)")
    print("2. CLI Mode (test mode, no Discord needed)")
    print("3. Exit")

    while True:
        choice = input("\nEnter choice (1/2/3): ").strip()

        if choice == "1":
            return "discord"
        elif choice == "2":
            return "cli"
        elif choice == "3":
            return "exit"
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


def check_dependencies():
    """Check if required Python packages are installed"""
    print("🔍 Checking Python dependencies...")

    required_packages = {
        'discord': 'discord.py',
        'dotenv': 'python-dotenv',
        'httpx': 'httpx',
        'mcp': 'mcp',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl'
    }

    missing = []

    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"⚠️  Missing dependencies: {', '.join(missing)}")
        print("\n📦 Installing missing dependencies...")
        print("⏳ This may take a few minutes...\n")

        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
                capture_output=True,
                text=True
            )
            print("✅ Dependencies installed successfully!\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies!")
            print(f"Error: {e.stderr}")
            print("\n💡 Please run manually: pip install -r requirements.txt")
            return False
    else:
        print("✅ All dependencies installed\n")
        return True


def check_env_file():
    """Check if .env file exists"""
    env_path = Path(".env")
    if not env_path.exists():
        print("\n⚠️  .env file not found!")
        print("📝 Creating .env from .env.example...")

        example_path = Path(".env.example")
        if example_path.exists():
            import shutil
            shutil.copy(example_path, env_path)
            print("✅ .env file created. Please edit it with your settings.")
        else:
            print("❌ .env.example not found. Please create .env manually.")

        return False
    return True


def run_bot(mode):
    """Run the bot in specified mode"""
    global BOT_PROCESS

    if mode == "discord":
        print("\n🚀 Starting Discord bot...")
        print("Press Ctrl+C to stop\n")
        print("="*60 + "\n")

        try:
            # Use Popen to track the process
            BOT_PROCESS = subprocess.Popen(["python", "bot.py"])
            BOT_PROCESS.wait()  # Wait for it to finish
        except KeyboardInterrupt:
            print("\n\n⚠️  Bot stopped by user")
            if BOT_PROCESS:
                BOT_PROCESS.terminate()
                try:
                    BOT_PROCESS.wait(timeout=5)
                except:
                    BOT_PROCESS.kill()
        except Exception as e:
            print(f"\n❌ Bot error: {e}")

    elif mode == "cli":
        print("\n🖥️  Starting CLI mode...")
        print("Press Ctrl+C to stop\n")
        print("="*60 + "\n")

        try:
            # Use Popen to track the process
            BOT_PROCESS = subprocess.Popen(["python", "cli_runner.py"])
            BOT_PROCESS.wait()  # Wait for it to finish
        except KeyboardInterrupt:
            print("\n\n⚠️  Bot stopped by user")
            if BOT_PROCESS:
                BOT_PROCESS.terminate()
                try:
                    BOT_PROCESS.wait(timeout=5)
                except:
                    BOT_PROCESS.kill()
        except Exception as e:
            print(f"\n❌ Bot error: {e}")


def main():
    """Main launcher function"""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Register cleanup function to run on exit
    atexit.register(cleanup_services)

    print_header()

    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n⚠️  Please install dependencies first!")
        input("Press Enter to exit...")
        return

    # Step 2: Check .env file
    if not check_env_file():
        print("\n⚠️  Please configure .env file first!")
        input("Press Enter to exit...")
        return

    # Step 3: Check if Ollama is installed
    print("🔍 Checking Ollama installation...")
    if not check_ollama_installed():
        print("❌ Ollama is not installed!")
        print("\n📥 Please install Ollama from: https://ollama.ai/download")
        input("\nPress Enter to exit...")
        return
    print("✅ Ollama is installed\n")

    # Step 4: Check if Ollama is running
    print("🔍 Checking Ollama server...")
    if check_ollama_running():
        print("✅ Ollama server is already running\n")
    else:
        print("❌ Ollama server is not running!")
        print("\n💡 Please start Ollama manually first:")
        print("   Run this command in a separate terminal: ollama serve")
        input("\nPress Enter to exit...")
        return

    # Step 5: Check if model is available
    model_name = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    print(f"🔍 Checking if model '{model_name}' is available...")

    if not check_model_available(model_name):
        print(f"⚠️  Model '{model_name}' not found")
        if not pull_model(model_name):
            input("\nPress Enter to exit...")
            return
    print(f"✅ Model '{model_name}' is ready\n")

    # Step 6: Automatically start Discord bot (no menu)
    print("🚀 Auto-starting Discord bot...")
    print("💡 Tip: To use CLI mode instead, run: python cli_runner.py\n")
    mode = "discord"

    # Step 7: Run the bot
    run_bot(mode)

    print("\n" + "="*60)
    print("👋 FinancialBot stopped")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Launcher interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)

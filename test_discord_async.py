"""
Quick test to verify async handling doesn't block
"""

import asyncio
import time
import sys
import codecs

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


async def simulate_long_task():
    """Simulates the web search that takes ~13 seconds"""
    print("Starting long task...")
    await asyncio.sleep(2)  # Simulate work
    print("Long task completed")
    return "Result from long task"


async def simulate_heartbeat():
    """Simulates Discord heartbeat every 5 seconds"""
    for i in range(5):
        await asyncio.sleep(5)
        print(f"💓 Heartbeat {i+1} - {time.strftime('%H:%M:%S')}")


async def simulate_message_handler():
    """Simulates the Discord on_message handler"""
    print("Message received, processing...")

    # Get event loop and run long task in executor (like we did in bot.py)
    loop = asyncio.get_event_loop()

    # Simulate the ThreadPoolExecutor approach
    def sync_long_task():
        import time
        time.sleep(2)
        return "Sync result"

    result = await loop.run_in_executor(None, sync_long_task)
    print(f"Got result: {result}")
    return result


async def main():
    """Run both tasks concurrently"""
    print("=" * 60)
    print("Testing async execution - heartbeat should NOT be blocked")
    print("=" * 60)

    # Run heartbeat and message handler concurrently
    await asyncio.gather(
        simulate_heartbeat(),
        simulate_message_handler()
    )

    print("\n✅ Test complete - if heartbeats continued, async works!")


if __name__ == "__main__":
    asyncio.run(main())

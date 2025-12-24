
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def main():
    print("🚀 Starting Complete Real-World Test...")
    from real_world.complete_working import complete_working_test
    await complete_working_test()

if __name__ == "__main__":
    asyncio.run(main())
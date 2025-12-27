import asyncio
from src.config.database import init_db

async def main():
    """Initialize the database tables"""
    print("Initializing database tables...")
    await init_db()
    print("Database tables initialized successfully!")

if __name__ == "__main__":
    asyncio.run(main())
import uvicorn
import asyncio
from src.api.baseapp import app
from src.models.db_connection import AsyncSessionGenerator, Base

async def create_tables():
    """Create database tables on startup"""
    session_gen = AsyncSessionGenerator()
    async with session_gen.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")

def main():
    # Create tables before starting the server
    asyncio.run(create_tables())
    
    # Start the FastAPI server
    uvicorn.run(
        "src.api.baseapp:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main()

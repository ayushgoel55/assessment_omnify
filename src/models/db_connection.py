from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from src.utils.singleton import singleton
from src.models.session_yeild import SessionGenerator  # abstract base class

DATABASE_URL = "sqlite+aiosqlite:///sqlite_database.db"

Base = declarative_base()

@singleton
class AsyncSessionGenerator(SessionGenerator):
    def __init__(self):
        self.engine = create_async_engine(
            DATABASE_URL,
            echo=True,
            future=True
        )

        self.async_session = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )


    async def get_session(self) :
        async with self.async_session() as session:
            yield session

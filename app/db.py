from app.config import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


engine = create_async_engine(config.db_string)
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

__all__ = ["engine", "async_session"]

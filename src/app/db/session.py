from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from app.configs import settings

engine: AsyncEngine = create_async_engine(
    settings.db_url
)

AsyncLocalSession: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncLocalSession() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

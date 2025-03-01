import logging
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from tenacity import after_log  # type: ignore
from tenacity import before_log  # type: ignore
from tenacity import stop_after_attempt  # type: ignore
from tenacity import wait_fixed  # type: ignore
from tenacity import retry

from stormpiper.core.config import settings

logging.basicConfig(level=settings.LOGLEVEL)
logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL_SYNC, pool_recycle=settings.DATABASE_POOL_RECYCLE
)


_there_can_be_only_one = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    if _there_can_be_only_one is None:
        async_engine = create_async_engine(
            settings.DATABASE_URL_ASYNC, pool_recycle=settings.DATABASE_POOL_RECYCLE
        )
        async_session_maker = sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )
    else:
        async_session_maker = _there_can_be_only_one

    async with async_session_maker() as session:
        yield session


def get_session(engine=engine):
    return sessionmaker(engine, autocommit=False, autoflush=False)


@retry(
    stop=stop_after_attempt(60 * 5),  # 5 mins
    wait=wait_fixed(2),  # 2 seconds
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def reconnect_engine(engine=engine):
    try:
        with engine.begin() as conn:
            # this should connect/login and ensure that the database is available.
            conn.execute("select 1").fetchall()

    except Exception as e:
        logger.error(e)
        logger.info("Engine connection url:", engine.url)
        raise e

import logging
import asyncio
import platform

import redis
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

import stormpiper.bg_worker as bg
from stormpiper.core.config import settings
from stormpiper.database.connection import engine
from stormpiper.database.utils import reconnect_engine
from stormpiper.apps.supersafe.init_users import create_admin

wait_seconds = 2
try_for_minutes = 5
max_tries = int(60 / wait_seconds * try_for_minutes)


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

redis_conn = redis.Redis(host="redis", port=6379)


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def get_background_worker_connection():  # pragma: no cover
    try:
        bg.ping.apply_async().get(timeout=0.2)
    except Exception as e:
        logger.error(e)
        raise e


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def get_redis_connection():  # pragma: no cover
    try:
        assert redis_conn.ping()
    except Exception as e:
        logger.error(e)
        raise e


def get_database_connection():
    reconnect_engine(engine)


def create_admin_user() -> None:
    logger.info("Creating initial data")

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_admin())

    logger.info("Initial data created")

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

from config import get_settings

settings = get_settings()


def pydantic_serializer(value):
    json_method = getattr(value, "json", None)
    if callable(json_method):
        return value.json()
    return value


async_engine = create_async_engine(
    settings.DB_ASYNC_CONNECTION_STR,
    echo=True,
    future=True,
    json_serializer=pydantic_serializer,
)

async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
    info=None,
)


async def get_async_session():
    async with async_session() as session:
        yield session


if settings.DEBUG:
    logging.basicConfig()
    logger = logging.getLogger("MY_APP_NAME.sqltime")
    logger.setLevel(logging.DEBUG)

    @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(
        conn,
        cursor,
        statement,
        parameters,
        context,
        executemany,
    ):
        conn.info.setdefault("query_start_time", []).append(time.time())
        logger.debug("Start Query: %s", statement)

    @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(
        conn,
        cursor,
        statement,
        parameters,
        context,
        executemany,
    ):
        total = time.time() - conn.info["query_start_time"].pop(-1)
        logger.debug("Query Complete!")
        logger.debug("Total Time: %f", total)

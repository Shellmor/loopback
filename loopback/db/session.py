import functools
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from contextvars import ContextVar, Token
from uuid import uuid4
from core.config import settings

session_context: ContextVar[str] = ContextVar("session_context")

engine = create_async_engine(settings.DATABASE_URL.unicode_string())
async_session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)
session = AsyncSession(engine)

def get_session_context() -> str:
    return session_context.get()


def set_session_context(session_id: str) -> Token:
    return session_context.set(session_id)


def reset_session_context(context: Token) -> None:
    session_context.reset(context)


def async_standalone_session(func):
    @functools.wraps(func)
    async def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            return func(*args, **kwargs)
        finally:
            await session.close()
            reset_session_context(context=context)

    return _standalone_session
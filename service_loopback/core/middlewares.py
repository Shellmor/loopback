from uuid import uuid4

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.middleware.base import BaseHTTPMiddleware
from db.session import reset_session_context, session, set_session_context


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await self.app(scope, receive, send)
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
            reset_session_context(context=context)

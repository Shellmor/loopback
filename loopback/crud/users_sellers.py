from sqlalchemy import and_, or_

from sqlalchemy.future import select

from db.models import UsersSellers
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users_sellers import CreateUsersSellers, UpdateUsersSellers
from db.session import async_session
from .base import CRUDBase
from api import exceptions as exc


class CRUDUsersSellers(CRUDBase):
    model: UsersSellers

    async def check_user_in_context(self, context: str, user_id: int, session: AsyncSession) -> UsersSellers:
        query = select(self.model).filter(self.model.context == context, self.model.id == user_id)  # type: ignore
        user = await session.execute(query)
        result = user.scalar()
        return result

    async def check_user_duplicate(self, context: str, email: str, username: str, session: AsyncSession) -> UsersSellers:
        query = select(self.model).filter(
            and_(self.model.context == context, or_(self.model.email == email or self.model.username == username)) # type: ignore
        )
        user = await session.execute(query)
        result = user.scalar()
        return result

    async def get_users_list_in_context(self, context: str):
        async with async_session() as session:
            query = select(self.model).filter(self.model.context == context).order_by(self.model.created.desc()) # type: ignore
            result = await session.execute(query)
            return result.scalars().all()

    async def get_user_in_context_by_id(self, context: str, user_seller_id: int):
        async with async_session() as session:
            result = await self.check_user_in_context(context, user_seller_id, session)
            if not result:
                raise exc.UserContextNotFound(user_seller_id, context)
            return result

    async def create_users_in_context(self, context: str, obj_in: CreateUsersSellers):
        async with async_session() as session:
            check_duplicate = await self.check_user_duplicate(context, obj_in.email, obj_in.username, session)
            if check_duplicate:
                raise exc.StoreUserConflictError
            result = await super().create(session, obj_in)
            return result

    async def update_users_in_context(self, context: str, user_seller_id: int, obj_in: UpdateUsersSellers):
        async with async_session() as session:
            user = await self.check_user_in_context(context, user_seller_id, session)
            if not user:
                raise exc.UserContextNotFound(user_seller_id, context)
            check_duplicate = await self.check_user_duplicate(context, obj_in.email, obj_in.username, session)
            if check_duplicate:
                raise exc.StoreUserConflictError
            result = await super().update(user_seller_id, session, obj_in)
            return result

    async def delete_users_in_context(self, context: str, user_seller_id: int):
        async with async_session() as session:
            user = await self.check_user_in_context(context, user_seller_id, session)
            if not user:
                raise exc.UserContextNotFound(user_seller_id, context)
            result = await super().remove(session, user_seller_id)
            return result

users_sellers_crud = CRUDUsersSellers(UsersSellers)

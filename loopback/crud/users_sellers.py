from sqlalchemy.future import select

from db.models import UsersSellers
from db.session import async_session
from .base import CRUDBase


class CRUDUsersSellers(CRUDBase):
    model: UsersSellers

    async def get_users_list(self, context: str):
        async with async_session() as session:
            query = select(self.model).filter(self.model.context == context) # type: ignore
            result = await session.execute(query)
            return result.scalars().all()


users_sellers_crud = CRUDUsersSellers(UsersSellers)

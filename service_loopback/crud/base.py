from typing import Generic, Type, TypeVar, Optional, Any, Sequence

from pydantic import BaseModel
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api import exceptions as exc

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, obj_id: int) -> Optional[ModelType]:
        """ Получает объект по ID. """

        result = await session.get(self.model, obj_id)
        return result

    async def get_multi(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> Sequence[Row[Any] | RowMapping | Any]:
        """ Получает список объектов с возможностью пропуска и лимита. """

        query = select(self.model).offset(skip).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    async def create(self, session: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        """ Создает новый объект. """

        obj = self.model(**obj_in.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    async def update(self, obj_id: int, session: AsyncSession, obj_in: UpdateSchemaType | dict) -> ModelType:
        """ Обновить существующий объект. """

        db_obj = await session.get(self.model, obj_id)
        if not db_obj:
            raise exc.ObjectNotFound(obj_id)
        obj_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BaseModel) else obj_in
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, obj_id: int) -> Optional[ModelType]:
        """ Удаляет объект по ID. """

        obj = await session.get(self.model, obj_id)
        if obj:
            await session.delete(obj)
            await session.commit()
        return obj


crud_base = CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]

from datetime import datetime
from typing import List

from pydantic import BaseModel

from core.utils import creating_model_with_optional_fields
from .base import PaginatedBase


class UsersSellersBase(BaseModel):
    username: str
    first_name: str | None
    last_name: str | None
    email: str
    created: datetime
    status: str
    context: str

class CreateUsersSellers(UsersSellersBase):
    pass

UpdateUsersSellers = creating_model_with_optional_fields("UpdateUsersSellers", UsersSellersBase)

class UsersSellersOut(UsersSellersBase):
    id: int

class UsersSellersOutPaginated(PaginatedBase):
    list: list[UsersSellersOut]

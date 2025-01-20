from lib2to3.fixes.fix_input import context
from typing import Any

from fastapi import HTTPException, status


class BaseExceptionSend(HTTPException):
    status_code: int = None
    detail: Any = None

    def __init__(self) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail)

class Conflict(BaseExceptionSend):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Conflict"

class NotFound(BaseExceptionSend):
    status_code: int = status.HTTP_404_NOT_FOUND
    detail: str = None

class BadRequest(BaseException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = None

class StoreUserConflictError(Conflict):
    detail: str = f"Пользователь с такими данными уже существует в этом магазине."

class ObjectNotFound(NotFound):
    def __init__(self, user_id: int):
        self.detail = f"Объект с id {user_id} не существует."
        super().__init__()

class UserContextNotFound(NotFound):
    def __init__(self, user_id: int, context_org: str):
        self.detail = f"Пользоватля с id {user_id} в магазине {context_org} не существует."
        super().__init__()


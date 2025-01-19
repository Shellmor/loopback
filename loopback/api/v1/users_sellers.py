from fastapi import APIRouter, Depends

from crud.users_sellers import users_sellers_crud
from schemas.base import PaginationParams
from schemas.users_sellers import UsersSellersOutPaginated
from api import paginate

router = APIRouter()

@router.get("/{context}/users_sellers", response_model=UsersSellersOutPaginated, name="Получить все панели мониторинга"
            )
async def get_list_users_sellers(
        context: str,
        params: PaginationParams = Depends(),
):
    result = await users_sellers_crud.get_users_list(context)
    response_paginate = await paginate(result, params)
    return response_paginate


# @router.post("/{context}/users_sellers")
# async def create_users_sellers(users: UsersSellers):
#     #TODO: The function should work as an email invitation.
#     result = await users_sellers_crud.create_users(users)
#     return result
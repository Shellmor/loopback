from fastapi import APIRouter, Depends

from api import paginate
from crud.users_sellers import users_sellers_crud
from schemas.base import PaginationParams
from schemas.users_sellers import UsersSellersOutPaginated, CreateUsersSellers, UsersSellersOut, UpdateUsersSellers

router = APIRouter()

@router.get("/{context}/users_sellers", response_model=UsersSellersOutPaginated)
async def get_list_users_sellers(
        context: str,
        params: PaginationParams = Depends(),
):
    """ Получает список продавцов магазина """

    result = await users_sellers_crud.get_users_list_in_context(context)
    response_paginate = await paginate(result, params)
    return response_paginate

@router.get("/{context}/users_sellers/{user_seller_id}", response_model=UsersSellersOut)
async def get_user_seller(
        context: str,
        user_seller_id: int
):
    """ Получает продавца магазина по его ID """

    result = await users_sellers_crud.get_user_in_context_by_id(context, user_seller_id)
    return result


@router.post("/{context}/users_sellers",response_model=UsersSellersOut, status_code=201)
async def create_users_sellers(
        context: str,
        obj_in: CreateUsersSellers
):
    """ Создает продавца в магазине"""

    result = await users_sellers_crud.create_users_in_context(context, obj_in)
    return result


@router.patch("/{context}/users_sellers/{user_seller_id}", response_model=UsersSellersOut)
async def update_users_sellers(
        context: str,
        user_seller_id: int,
        obj_in: UpdateUsersSellers
):
    """ Изменяет продавца в магазине по его ID"""

    result = await users_sellers_crud.update_users_in_context(context, user_seller_id, obj_in)
    return result

@router.delete("/{context}/users_sellers/{user_seller_id}")
async def delete_users_sellers(
        context: str,
        user_seller_id: int
):
    """ Удаляет продавца в магазине """
    await users_sellers_crud.delete_users_in_context(context, user_seller_id)
    return True


from schemas.base import PaginatedBase, PaginatedMeta, PaginationParams

async def paginate(answer: list, params: PaginationParams) -> PaginatedBase:
    page = params.page
    per_page = params.per_page

    total_count = len(answer)
    result = PaginatedBase(
        meta=PaginatedMeta(page=page, per_page=per_page, total_count=total_count),
        list=answer[per_page * (page - 1):per_page * page]
    )
    return result

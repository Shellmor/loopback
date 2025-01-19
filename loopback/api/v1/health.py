from fastapi import APIRouter
import asyncio
router = APIRouter()


@router.get("/health")
async def healthcheck():
    await asyncio.sleep(1)
    return {'status': 'ok'}

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.users_handlers import router as users_router
from app.db.session import get_session

api_router = APIRouter(prefix='/v1', tags=['api'])
api_router.include_router(users_router)


@api_router.get('/healthcheck')
async def get_healthcheck(session: AsyncSession = Depends(get_session)):
    await session.execute(text('SELECT 1'))
    return {'message': 'Service works!'}


__all__ = [
    'api_router'
]

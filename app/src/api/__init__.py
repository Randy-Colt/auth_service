from fastapi import APIRouter

from src.api.auth_handlers import router as auth_router

api_router = APIRouter(prefix='/v1')
api_router.include_router(auth_router)


@api_router.get('/healthcheck')
async def get_healthcheck():
    return {'message': 'Service works!'}


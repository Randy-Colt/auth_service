from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.schemas.users import CreateUserSchema, UserSchema
from src.services.users import UserService
from src.services import exceptions as service_exc
from src.utils.jwt_encoding import encode_jwt
from src.api.dependencies.service_factory import get_user_service


router = APIRouter(prefix='/users', tags=['api', 'users'])


@router.get('/')
async def get_users(
    user_service: UserService = Depends(get_user_service)
) -> list[UserSchema]:
    return await user_service.get_users()


@router.post('/aquire')
async def aquire_user(
    user_id: UUID,
    user_servise: UserService = Depends(get_user_service)
) -> UserSchema:
    try:
        user = await user_servise.aquire_lock(user_id)
    except service_exc.UserIsBusyException as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.message
        )
    except service_exc.UserNotFoundException as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            e.message
        )
    return user


@router.post('/release')
async def release_user(
    user_id: UUID,
    user_servise: UserService = Depends(get_user_service)
) -> UserSchema:
    try:
        user = await user_servise.release_lock(user_id)
    except service_exc.UserNotFoundException as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            e.message
        )
    return user


@router.post('/create')
async def create_user(user_schema: CreateUserSchema):
    return

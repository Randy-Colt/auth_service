from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import OperationalError

from app.api.dependencies.service_factory import get_user_service
from app.schemas.auth import TokenSchema
from app.schemas.users import CreateUserSchema, UserSchema
from app.services import exceptions as service_exc
from app.services.users import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_users(
    user_service: UserService = Depends(get_user_service)
) -> list[UserSchema]:
    """Возвращает список всех существующих пользователей."""
    return await user_service.get_users()


@router.patch('/aquire')
async def aquire_user(
    user_id: UUID,
    response: Response,
    user_servise: UserService = Depends(get_user_service)
) -> TokenSchema:
    """
    Захватить юзера для проведения тестов.

    :param user_id: id пользователя, которого нужно захватить
    :return: jwt-токен возвращается в ответе и устанавливается в заголовок
    Authorization ответа.
    """
    try:
        token = await user_servise.aquire_lock(user_id)
    except service_exc.UserIsBusyException as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.message
        )
    except OperationalError:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            'Пользователь в обработке, попробуйте позже'
        )
    except service_exc.UserNotFoundException as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            e.message
        )
    response.headers['Authorization'] = (
        f'{token.token_type} {token.access_token}'
    )
    return token


@router.patch('/release')
async def release_user(
    user_id: UUID,
    user_servise: UserService = Depends(get_user_service)
) -> UserSchema:
    """
    Освободить юзера.

    Сработает даже если locktime юзера None.
    :param user_id: id юзера, которого следует освододить
    :return: данные освобождённого пользователя.
    """
    try:
        user = await user_servise.release_lock(user_id)
    except service_exc.UserNotFoundException as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            e.message
        )
    return user


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(
    user_schema: CreateUserSchema,
    user_servise: UserService = Depends(get_user_service)
) -> UserSchema:
    """
    Создать нового пользователя.

    :return: данные созданного пользователя.
    """
    try:
        return await user_servise.create_user(user_schema)
    except service_exc.LoginAlreadyExistsException as e:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            e.message
        )

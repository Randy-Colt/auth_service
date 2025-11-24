from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.users import UserRepository
from app.db.session import get_session
from app.services.users import UserService


def get_user_repository(
    session: AsyncSession = Depends(get_session)
):
    return UserRepository(session)


def get_user_service(
    user_repo: UserRepository = Depends(get_user_repository)
):
    return UserService(user_repo)

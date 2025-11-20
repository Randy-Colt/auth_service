from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.db.session import get_session
from src.crud.users import UserRepository


def get_auth_repository(
    session: AsyncSession = Depends(get_session)
):
    return UserRepository(session)

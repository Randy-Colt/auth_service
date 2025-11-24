from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Column, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import exceptions as crud_exc
from app.db.models import User


@dataclass(slots=True, eq=False, frozen=True)
class UserRepository:
    """Репозиторий для выполнения операций с базой данных."""

    session: AsyncSession

    async def create_user(self, user_schema: dict[str, Any]) -> User:
        """
        Создаёт юзера согласно необходимым полям.

        Если login уже существует в базе, выбрасывает LoginExistsException.
        """
        user = User(**user_schema)
        self.session.add(user)
        try:
            await self.session.commit()
        except IntegrityError as e:
            if str(e.orig).endswith('login'):
                raise crud_exc.LoginExistsException
        await self.session.refresh(user)
        return user

    async def set_locktime(self, uuid: UUID) -> User:
        """
        Устанавливает временную метку.

        Если пользователь уже в обработке, выбрасывает OperationalError
        """
        try:
            result = await self.session.execute(
                select(User).where(User.id == uuid)
                .with_for_update(nowait=True)
            )
            user = result.scalar_one()
        except NoResultFound:
            raise crud_exc.NoResultFoundException

        if user.locktime is not None:
            raise crud_exc.LocktimeIsntNoneException

        user.locktime = datetime.now()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def set_locktime_to_null(self, uuid: UUID) -> User:
        """Обнуляет locktime."""
        result = await self.session.execute(
            select(User).where(User.id == uuid)
        )
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise crud_exc.NoResultFoundException

        if user.locktime is None:
            return user

        user.locktime = None
        await self.session.commit()
        return user

    async def get_users(self, schema_type: BaseModel) -> list[dict[str, Any]]:
        """Получает всех существующих пользователей в виде списка словарей."""
        result = await self.session.execute(
            select(*self._select_user_by_schema(schema_type))
        )
        return result.mappings().all()

    def _select_user_by_schema(self, schema_type: BaseModel) -> list[Column]:
        """
        Согласно переданной схеме возвращает список атрибутов,
        которые нужно передать в select.
        """
        return [
            getattr(User, attr) for attr in schema_type.__annotations__.keys()
            if hasattr(User, attr)
        ]

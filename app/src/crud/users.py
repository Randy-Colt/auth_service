from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, select
from sqlalchemy.exc import OperationalError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import CreateUserSchema, UserSchema
from src.services import exceptions as service_exc
from src.db.models import User


@dataclass(slots=True)
class UserRepository:
    session: AsyncSession

    async def create_user(self, user_schema: CreateUserSchema) -> UserSchema:
        user = User(**user_schema.model_dump())
        await self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserSchema.model_validate(user)

    async def set_locktime(self, uuid: UUID) -> UserSchema | None:
        try:
            result = await self.session.execute(
                select(
                    *self._select_user_by_schema()
                ).where(User.id == uuid).with_for_update(nowait=True)
            )
            user = result.scalar_one()
        except OperationalError:
            raise service_exc.UserIsBusyException
        except NoResultFound:
            raise service_exc.UserNotFoundException

        if user.locktime is None:
            return UserSchema.model_validate(user)

        user.locktime = datetime.now()
        await self.session.commit()
        await self.session.refresh(user)
        return UserSchema.model_validate(user)

    async def set_locktime_to_null(self, uuid: UUID) -> UserSchema | None:
        result = await self.session.execute(
            select(
                *self._select_user_by_schema()
            ).where(User.id == uuid)
        )
        try:
            user = result.scalar_one()
        except NoResultFound:
            raise service_exc.UserNotFoundException

        user_result = UserSchema.model_validate(user)

        if user.locktime is None:
            return user_result

        user.locktime = None
        await self.session.commit()
        return user_result

    async def get_users(self) -> list[UserSchema]:
        result = await self.session.execute(
            select(*self._select_user_by_schema())
        )
        users = result.mappings().all()
        return [UserSchema(**user) for user in users]

    def _select_user_by_schema(self) -> list[Column]:
        return [
            getattr(User, attr) for attr in UserSchema.__annotations__.keys()
            if hasattr(User, attr)
        ]


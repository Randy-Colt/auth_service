from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.users import CreateUserSchema, UserSchema
from src.db.models import User

@dataclass(slots=True)
class UserRepository:
    session: AsyncSession

    async def create_user(self, user_schema: CreateUserSchema) -> UserSchema:
        user = User(**user.model_dump())
        await self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserSchema.model_validate(user)

    async def set_locktime(self, uuid: UUID) -> UserSchema | None:
        try:
            result = await self.session.execute(
                select(User).where(User.id == uuid).with_for_update(nowait=True)
            )
            user = result.scalar_one()
        except OperationalError:
            return None

        if user.locktime is None:
            return None

        user.locktime = datetime.now()
        await self.session.commit()
        await self.session.refresh(user)
        return UserSchema.model_validate(user)

    async def set_locktime_to_null(self, uuid: UUID) -> UserSchema | None:
        result = await self.session.execute(
            select(User).where(User.id == uuid)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return None

        user_result = UserSchema.model_validate(user)

        if user.locktime is None:
            return user_result

        user.locktime = None
        await self.session.commit()
        return user_result

from dataclasses import dataclass
from uuid import UUID

from src.crud.users import UserRepository
from src.schemas.users import CreateUserSchema, UserSchema


@dataclass(slots=True)
class UserService:
    user_repo: UserRepository

    async def create_user(self, user_schema: CreateUserSchema) -> UserSchema:
        return await self.user_repo.create(user_schema)

    async def get_users(self) -> list[UserSchema]:
        return await self.user_repo.get_users()

    async def aquire_lock(self, user_id: UUID) -> UserSchema:
        return await self.user_repo.set_locktime(user_id)

    async def release_lock(self, user_id: UUID) -> UserSchema:
        return await self.user_repo.set_locktime_to_null(user_id)

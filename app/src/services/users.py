from dataclasses import dataclass, field
from uuid import UUID

from src.crud.users import UserRepository
from src.schemas.users import CreateUserSchema, UserSchema
from src.services.dependencies.sessions import get_auth_repository


@dataclass(slots=True)
class UserService:
    user_repo: UserRepository = field(default_factory=get_auth_repository)

    async def create_user(self, user_schema: CreateUserSchema) -> UserSchema:
        user = await self.user_repo.create(user_schema)
        return user

    async def aquire(self, user_id: UUID) -> UserSchema | str:
        user = await self.user_repo.set_locktime(user_id)

        if user is None:
            return 'Пользователь с этим id занят'

        return user
    
    async def release(self, user_id: UUID):
        user = await self.user_repo.set_locktime_to_null(user_id)

        if user is None:
            return 'Такого пользователя не существует'

        return user

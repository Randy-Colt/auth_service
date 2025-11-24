from dataclasses import dataclass
from uuid import UUID

from app.crud import exceptions as crud_exc
from app.crud.users import UserRepository
from app.schemas.auth import TokenSchema
from app.schemas.users import CreateUserSchema, UserSchema
from app.services import exceptions as service_exc
from app.utils import encode_jwt, hash_password


@dataclass(slots=True, eq=False)
class UserService:
    user_repo: UserRepository

    async def create_user(self, user_schema: CreateUserSchema) -> UserSchema:
        user_dict = user_schema.model_dump(exclude={'password'})
        hashed_password = hash_password(
            user_schema.password.get_secret_value()
        )
        user_dict['password'] = hashed_password
        try:
            user = await self.user_repo.create_user(user_dict)
        except crud_exc.LoginExistsException:
            raise service_exc.LoginAlreadyExistsException

        return UserSchema.model_validate(user)

    async def get_users(self) -> list[UserSchema]:
        users = await self.user_repo.get_users(UserSchema)
        return [UserSchema.model_validate(user) for user in users]

    async def aquire_lock(self, user_id: UUID) -> TokenSchema:
        try:
            user = await self.user_repo.set_locktime(user_id)
        except crud_exc.NoResultFoundException:
            raise service_exc.UserNotFoundException
        except crud_exc.LocktimeIsntNoneException:
            raise service_exc.UserIsBusyException

        payload = UserSchema.model_validate(user).model_dump(
            include={'id', 'project_id'}
        )
        payload['id'] = str(payload['id'])
        payload['project_id'] = str(payload['project_id'])
        token = encode_jwt(payload)
        return TokenSchema(access_token=token)

    async def release_lock(self, user_id: UUID) -> UserSchema:
        try:
            user = await self.user_repo.set_locktime_to_null(user_id)
        except crud_exc.NoResultFoundException:
            raise service_exc.UserNotFoundException

        return UserSchema.model_validate(user)

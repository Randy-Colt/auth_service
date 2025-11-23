from enum import StrEnum
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    PastDatetime,
    UUID4,
    SecretStr
)


class EnvEnum(StrEnum):
    PROD = 'prod'
    PREPOD = 'prepod'
    STAGE = 'stage'


class DomainEnum(StrEnum):
    CANARY = 'canary'
    REGULAR = 'regular'


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    project_id: UUID4
    env: EnvEnum
    domain: DomainEnum
    created_at: PastDatetime
    locktime: PastDatetime | None


class CreateUserSchema(BaseModel):

    login: EmailStr
    password: Annotated[SecretStr, MaxLen(15), MinLen(8)]
    project_id: UUID4
    env: EnvEnum
    domain: DomainEnum

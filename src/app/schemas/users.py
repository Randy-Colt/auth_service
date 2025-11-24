from enum import StrEnum
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import (UUID4, BaseModel, ConfigDict, EmailStr, PastDatetime,
                      SecretStr)


class EnvEnum(StrEnum):
    """Возможные значения для User.env."""

    PROD = 'prod'
    PREPOD = 'prepod'
    STAGE = 'stage'


class DomainEnum(StrEnum):
    """Возможные значения для User.domain."""

    CANARY = 'canary'
    REGULAR = 'regular'


class UserSchema(BaseModel):
    """Схема с основными данными пользователя"""

    model_config = ConfigDict(from_attributes=True)

    id: UUID4
    project_id: UUID4
    env: EnvEnum
    domain: DomainEnum
    created_at: PastDatetime
    locktime: PastDatetime | None


class CreateUserSchema(BaseModel):
    """Схема с необходимыми для создания пользователя полями"""

    login: EmailStr
    password: Annotated[SecretStr, MaxLen(15), MinLen(8)]
    project_id: UUID4
    env: EnvEnum
    domain: DomainEnum

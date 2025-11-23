import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.services.users import UserService
from app.schemas.users import CreateUserSchema, UserSchema
from app.schemas.auth import TokenSchema


@pytest.mark.asyncio
async def test_create_user():
    # arrange
    user_repo = AsyncMock()
    service = UserService(user_repo)

    schema = CreateUserSchema(
        login="test@example.com",
        password="StrongPass1!",
        project_id=uuid4(),
        env="prod",
        domain="regular"
    )

    fake_db_user = {
        "id": uuid4(),
        "project_id": schema.project_id,
        "env": schema.env,
        "domain": schema.domain,
        "created_at": "2024-01-01T00:00:00",
        "locktime": None,
    }

    user_repo.create_user.return_value = fake_db_user

    with patch("src.services.users.hash_password", return_value="HASHED"):
        # act
        result = await service.create_user(schema)

    # assert
    user_repo.create_user.assert_awaited_once()
    assert isinstance(result, UserSchema)
    assert result.project_id == schema.project_id


@pytest.mark.asyncio
async def test_get_users():
    user_repo = AsyncMock()
    service = UserService(user_repo)

    fake_users = [
        {
            "id": uuid4(),
            "project_id": uuid4(),
            "env": "prod",
            "domain": "regular",
            "created_at": "2023-01-01T00:00:00",
            "locktime": None,
        }
    ]

    user_repo.get_users.return_value = fake_users

    result = await service.get_users()

    user_repo.get_users.assert_awaited_once()
    assert len(result) == 1
    assert isinstance(result[0], UserSchema)


@pytest.mark.asyncio
async def test_aquire_lock():
    user_repo = AsyncMock()
    service = UserService(user_repo)

    fake_user = {
        "id": uuid4(),
        "project_id": uuid4(),
        "env": "prod",
        "domain": "regular",
        "created_at": "2023-01-01T00:00:00",
        "locktime": None,
    }

    user_repo.set_locktime.return_value = fake_user

    with patch("src.services.users.encode_jwt", return_value="TOKEN123"):
        result = await service.aquire_lock(fake_user["id"])

    user_repo.set_locktime.assert_awaited_once_with(fake_user["id"])
    assert isinstance(result, TokenSchema)
    assert result.access_token == "TOKEN123"


@pytest.mark.asyncio
async def test_release_lock():
    user_repo = AsyncMock()
    service = UserService(user_repo)

    fake_user = {
        "id": uuid4(),
        "project_id": uuid4(),
        "env": "prod",
        "domain": "regular",
        "created_at": "2023-01-01T00:00:00",
        "locktime": None,
    }

    user_repo.set_locktime_to_null.return_value = fake_user

    result = await service.release_lock(fake_user["id"])

    user_repo.set_locktime_to_null.assert_awaited_once_with(fake_user["id"])
    assert isinstance(result, UserSchema)

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.crud import exceptions as crud_exc
from app.schemas.auth import TokenSchema
from app.schemas.users import CreateUserSchema, UserSchema
from app.services.exceptions import UserIsBusyException
from app.services.users import UserService
from app.utils import encode_jwt, hash_password


@pytest.fixture(scope='module')
def user_service():
    return UserService(AsyncMock())


@pytest.fixture(scope='module')
def create_schema():
    return CreateUserSchema(
        login='test@example.com',
        password='password',
        project_id=uuid4(),
        env='prod',
        domain='regular'
    )


@pytest.fixture(scope='module')
def user_dict(create_schema):
    return {
        'id': uuid4(),
        'project_id': create_schema.project_id,
        'env': create_schema.env,
        'domain': create_schema.domain,
        'created_at': '2025-11-11T00:00:00',
        'locktime': '2025-11-11T11:00:00',
    }


@pytest.fixture(scope='module')
def user_dict_locktime_none(create_schema):
    return {
        'id': uuid4(),
        'project_id': create_schema.project_id,
        'env': create_schema.env,
        'domain': create_schema.domain,
        'created_at': '2025-11-11T00:00:00',
        'locktime': None
    }


@pytest.mark.asyncio
async def test_create_user_with_correct_data(
    user_service,
    user_dict,
    create_schema
):
    user_service.user_repo.create_user.return_value = user_dict

    with patch('app.services.users.hash_password', return_value='HASHED'):
        result = await user_service.create_user(create_schema)

    user_service.user_repo.create_user.assert_awaited_once()
    assert isinstance(result, UserSchema)
    assert result.project_id == create_schema.project_id


def test_password_hashed():
    unhashed_password = 'password'

    result = hash_password(unhashed_password)

    assert unhashed_password != result.decode()


def test_encode_jwt_structure():
    jwt = encode_jwt(
        {'sub': 'username'},
        ('-----BEGIN EC PRIVATE KEY-----'
        'MHcCAQEEIKG90OgIgVUfwLoyNMRzA6lkyPe1kHTuumf+pgLiM0U8oAoGCCqGSM49'
        'AwEHoUQDQgAEM4VWo1ZWx5+uzvuEnqL+19T2DgvxxOpO86EATh6H/xFkIJijm5V5'
        'Pc+JiEEqX+Zd81BHOcPChfKnqFsnVip81g=='
        '-----END EC PRIVATE KEY-----'),
        'ES256',
        1
    )
    assert len(jwt.split('.')) == 3


@pytest.mark.asyncio
async def test_get_users(user_service, user_dict):
    fake_users = [user_dict]
    user_service.user_repo.get_users.return_value = fake_users

    result = await user_service.get_users()

    user_service.user_repo.get_users.assert_awaited_once()
    assert len(result) == 1
    assert isinstance(result, list)
    assert isinstance(result[0], UserSchema)


@pytest.mark.asyncio
async def test_aquire_lock(user_service, user_dict_locktime_none):
    user_service.user_repo.set_locktime.return_value = user_dict_locktime_none

    with patch('app.services.users.encode_jwt', return_value='TOKEN'):
        result = await user_service.aquire_lock(user_dict_locktime_none['id'])

    user_service.user_repo.set_locktime.assert_awaited_once_with(
        user_dict_locktime_none['id']
    )
    assert isinstance(result, TokenSchema)
    assert result.access_token == 'TOKEN'


@pytest.mark.asyncio
async def test_aquire_blocked_lock(user_service, user_dict):
    user_service.user_repo.set_locktime.side_effect = crud_exc.LocktimeIsntNoneException

    with patch('app.services.users.encode_jwt'):
        with pytest.raises(UserIsBusyException):
            await user_service.aquire_lock(user_dict['id'])


@pytest.mark.asyncio
async def test_release_lock(user_service, user_dict_locktime_none):
    user_service.user_repo.set_locktime_to_null.return_value = user_dict_locktime_none

    result = await user_service.release_lock(user_dict_locktime_none['id'])

    user_service.user_repo.set_locktime_to_null.assert_awaited_once_with(user_dict_locktime_none['id'])
    user_service.user_repo.set_locktime_to_null.reset_mock()
    assert isinstance(result, UserSchema)
    assert result.locktime is None


@pytest.mark.asyncio
async def test_release_none_lock(user_service, user_dict_locktime_none):
    user_service.user_repo.set_locktime_to_null.return_value = user_dict_locktime_none

    result = await user_service.release_lock(user_dict_locktime_none['id'])

    user_service.user_repo.set_locktime_to_null.assert_awaited_once_with(
        user_dict_locktime_none['id']
    )
    user_service.user_repo.set_locktime_to_null.reset_mock()
    assert isinstance(result, UserSchema)
    assert result.locktime is None

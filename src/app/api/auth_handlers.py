from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.schemas.auth import TokenSchema
from src.utils import encode_jwt
from src.api.dependencies.auth_validation import validate_auth_user


router = APIRouter(prefix='/auth', tags=['auth'])
opauth = OAuth2PasswordBearer


@router.post('/login')
async def auth_user(
    oath = Depends(opauth),
    user = Depends(validate_auth_user)
) -> TokenSchema:
    payload = {
        'login': user.login,
    }
    return {}

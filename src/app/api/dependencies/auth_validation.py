from fastapi import HTTPException, status

from src.utils import check_password

class Mock:
    password = 'qwerty'

def validate_auth_user(login: str, password: str) -> None:
    unauth_exc = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        'Неверный логин или пароль'
    )
    user = Mock()
    # user = get_by_login(login)

    if not user:
        raise unauth_exc

    if check_password(password, user.password):
        raise unauth_exc

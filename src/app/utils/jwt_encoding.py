from datetime import UTC, datetime, timedelta
from typing import Any

from jwt import encode

from app.configs import settings


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.algoritm,
    expire_minures: int = settings.access_token_expire_minutes
) -> str:
    """
    Обёртка для преобразования пэйлоада в jwt.

    Также устанавливает iat = время выпуска токена и
    exp = время, когда срок жизни токена истечёт.
    """
    to_encode = payload.copy()
    now = datetime.now(UTC)
    to_encode.update(
        exp=now + timedelta(minutes=expire_minures),
        iat=now
    )
    return encode(
        payload,
        private_key,
        algorithm
    )

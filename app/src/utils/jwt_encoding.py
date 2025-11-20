from datetime import datetime, timedelta, UTC
from typing import Any

from jwt import decode, encode

from src.configs import settings


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.private_key_path.read_text(),
    algorithm: str = settings.algoritm,
    expire_minures: int = settings.access_token_expire_minutes
) -> str:
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


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.public_key_path.read_text(),
    algorithm: str = settings.algoritm
) -> Any:
    return decode(token, public_key, [algorithm])

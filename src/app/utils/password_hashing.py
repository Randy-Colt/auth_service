from bcrypt import gensalt, hashpw


def hash_password(password: str) -> bytes:
    """Обёртка для хэширования пароля с солью."""
    return hashpw(password.encode(), gensalt())

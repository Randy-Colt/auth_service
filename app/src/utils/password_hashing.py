from bcrypt import checkpw, gensalt, hashpw


def hash_password(password: str) -> bytes:
    return hashpw(password.encode(), gensalt())


def check_password(password: str, hashed_password: bytes) -> bool:
    return checkpw(password, hashed_password)

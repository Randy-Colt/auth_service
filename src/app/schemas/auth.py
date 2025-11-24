from pydantic import BaseModel


class TokenSchema(BaseModel):
    """Схема для jwt-токена."""

    access_token: str
    token_type: str = 'Bearer'

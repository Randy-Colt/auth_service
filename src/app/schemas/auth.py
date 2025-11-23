from pydantic import BaseModel, ConfigDict


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

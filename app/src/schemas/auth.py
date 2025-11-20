from pydantic import BaseModel, ConfigDict


class TokenSchema(BaseModel):
    acces_token: str
    token_type: str = 'Bearer'

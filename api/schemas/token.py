from pydantic import BaseModel, Field


class Token(BaseModel):
    token_type: str = Field(default='bearer')


class AccessToken(Token):
    access_token: str


class AccessRefreshToken(AccessToken):
    refresh_token: str

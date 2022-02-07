from pydantic import BaseModel, Field

from swa.core import Config


class TokenInResponse(BaseModel):
    id: int
    token: str
    refresh_token: str
    expiry_at: int
    user_id: int

    class Config:
        orm_mode = True


class AuthInRequest(BaseModel):
    nick: str = Field(min_length=Config.NICK_MIN_LENGTH, max_length=Config.NICK_MAX_LENGTH)
    email: str
    password: str
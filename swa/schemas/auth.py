from pydantic import BaseModel, Field

from swa.schemas.users import UserInResponse
from swa.core import Config


class TokenInDb(BaseModel):
    id: int = None
    refresh_token: str
    access_level: int
    user_id: str


class TokenInResponse(TokenInDb):
    user: UserInResponse
    access_token: str
    expires_in: int

    class Config:
        orm_mode = True


class AuthInRequest(BaseModel):
    nick: str = Field(min_length=Config.NICK_MIN_LENGTH, max_length=Config.NICK_MAX_LENGTH)
    email: str
    password: str = Field(min_length=Config.PASSWORD_MIN_LENGTH)


class AuthInResponse(BaseModel):
    user_id: str
    nick: str
    email: str
    password_hash: str


class LoginInRequest(BaseModel):
    email: str
    password: str
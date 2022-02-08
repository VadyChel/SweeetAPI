import typing
from datetime import datetime
from pydantic import BaseModel, Field
from swa.core import Config


class UserInResponse(BaseModel):
    id: int
    nick: str
    email: str
    skin_url: typing.Optional[str]
    coins: int
    created_at: datetime
    access_level: int
    bloksy: int # In-game money

    class Config:
        orm_mode = True


class UserNickInRequest(BaseModel):
    new_nick: str = Field(max_length=Config.NICK_MAX_LENGTH, min_length=Config.NICK_MIN_LENGTH)

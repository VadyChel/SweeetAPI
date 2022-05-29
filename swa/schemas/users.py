import typing
from datetime import datetime
from pydantic import BaseModel, Field
from swa.core import Config


class Privilege(BaseModel):
    id: int
    name: str
    remove_time: int


class UserInResponse(BaseModel):
    id: str
    nick: str
    email: str
    skin_url: typing.Optional[str]
    coins: int
    created_at: datetime
    access_level: int
    privilege: typing.Optional[Privilege]

    class Config:
        orm_mode = True


class UserNickInRequest(BaseModel):
    new_nick: str = Field(max_length=Config.NICK_MAX_LENGTH, min_length=Config.NICK_MIN_LENGTH)


class BloksyBalance(BaseModel):
    id: int
    user_id: str
    server_id: int
    bloksy: int # In game money

    class Config:
        orm_mode = True


class BloksyBalanceInTop(BaseModel):
    id: int
    user_id: str
    server_id: int
    user_nick: str
    bloksy: int # In game money

    class Config:
        orm_mode = True
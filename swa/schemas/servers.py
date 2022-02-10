import typing
from datetime import datetime
from pydantic import BaseModel


class Mod(BaseModel):
    id: int
    name: str


class ServerInResponse(BaseModel):
    id: int
    name: str
    description: str
    mods: typing.List[Mod]
    image_url: typing.Optional[str]
    long_description: str
    info: dict
    specials: list

    class Config:
        orm_mode = True


class ServerStats(BaseModel):
    id: int
    server_id: int
    online: int
    tps: int
    time: datetime
    record_online: int
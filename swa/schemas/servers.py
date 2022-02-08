import typing
from pydantic import BaseModel


class Mod(BaseModel):
    id: int
    name: str


class ServerInResponse(BaseModel):
    id: int
    name: str
    description: str
    mods: typing.List[Mod]
    image_url: str
    info: dict
    specials: dict

    class Config:
        orm_mode = True
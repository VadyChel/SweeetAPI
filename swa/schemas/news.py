import typing
from datetime import datetime
from pydantic import BaseModel, Field


class NewsInResponse(BaseModel):
    id: int
    title: str
    text: str
    created_at: datetime
    edited_at: typing.Optional[datetime]
    author_id: int
    image_url: typing.Optional[str]

    class Config:
        orm_mode = True


class NewsInRequest(BaseModel):
    title: str
    text: str
    created_at: datetime = Field(default_factory=datetime.now, const=True)
    edited_at: typing.Optional[datetime] = None
    author_id: int = 0
    image_url: typing.Optional[str]


class NewsInRequestEdit(BaseModel):
    title: typing.Optional[str]
    text: typing.Optional[str]
    edited_at: datetime = Field(default_factory=datetime.now, const=True)
    image_url: typing.Optional[str]
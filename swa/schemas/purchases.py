import typing

from pydantic import BaseModel, Field
from datetime import datetime


class UserPurchaseInResponse(BaseModel):
    id: int
    user_id: int
    count: int # Count of blocks, if type privilege => this field = 0
    cost: int
    type: str # privilege or block
    bought_item: str
    bought_item_id: int
    time: datetime
    remove_time: typing.Optional[datetime] # end time of privilege

    class Config:
        orm_mode = True


class UserPurchaseInRequest(BaseModel):
    user_id: int
    cost: int
    count: int
    bought_item: str
    bought_item_id: int
    type: str
    time: datetime = Field(default_factory=datetime.now, const=True)
    remove_time: typing.Optional[datetime]
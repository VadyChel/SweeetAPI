from pydantic import BaseModel
from datetime import datetime


class UserPurchaseInResponse(BaseModel):
    id: int
    user_id: int
    cost: int
    time: datetime
    coins_number: int


class BlockPurchaseInResponse(BaseModel):
    id: int
    block_id: int
    count: int
    time: datetime
    coins_number: int
import typing
from datetime import datetime
from pydantic import BaseModel, Field


class CoinsLogsInResponse(BaseModel):
    id: int
    user_id: str
    time: datetime
    coins_count: int
    reason: str

    class Config:
        orm_mode = True


class CoinsLogsInRequest(BaseModel):
    user_id: str
    time: datetime = Field(default_factory=datetime.now, const=True)
    coins_count: int
    reason: str
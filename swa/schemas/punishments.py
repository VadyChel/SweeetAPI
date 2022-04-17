from pydantic import BaseModel
from datetime import datetime


class Punishment(BaseModel):
    id: int
    nick: str
    user_id: str
    reason: str
    server: str
    moderator: str
    type: str
    time: datetime
    remove_time: datetime

    class Config:
        orm_mode = True

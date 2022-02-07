from pydantic import BaseModel
from datetime import datetime


class Punishment(BaseModel):
    id: int
    nick: str
    reason: str
    server: str
    moderator: str
    type: str
    time: datetime
    remove_time: datetime

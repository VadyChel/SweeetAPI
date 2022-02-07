from pydantic import BaseModel


class UserInResponse(BaseModel):
    id: int
    nick: int
    email: int
    skin_url: str
    coins: int
    bloksy: int # In-game money
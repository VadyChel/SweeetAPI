from pydantic import BaseModel


class TokenInResponse(BaseModel):
    id: int
    token: str
    refresh_token: str
    expiry_at: int
    user_id: int

    class Config:
        orm_mode = True


class AuthInRequest(BaseModel):
    nick: str
    email: str
    password: str
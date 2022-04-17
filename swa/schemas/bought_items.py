from pydantic import BaseModel, Field


class BoughtItemInResponse(BaseModel):
    id: int
    minecraft_item_id: str
    count: int
    item_id: int
    item_name: str
    user_id: str

    class Config:
        orm_mode = True


class BoughtItemInRequest(BaseModel):
    minecraft_item_id: str
    count: int = Field(gt=0, lt=2368)
    item_id: int
    item_name: str
    user_id: str
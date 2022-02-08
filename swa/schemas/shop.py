from pydantic import BaseModel
from .servers import Mod


class ShopItemInResponse(BaseModel):
    id: int
    minecraft_block_id: int
    block_name: str
    mod: Mod
    cost: int
    max_count: int
    count_per_one_cost: int # Сколько блоков за одну стоимость
    specials: dict

    class Config:
        orm_mode = True


class BuyShopItem(BaseModel):
    block_id: int
    count: int
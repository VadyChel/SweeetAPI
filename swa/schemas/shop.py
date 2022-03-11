import typing
from pydantic import BaseModel
from .servers import Mod


class ShopItemInResponse(BaseModel):
    id: int
    minecraft_block_id: int
    block_name: str
    mod: Mod
    cost: typing.Dict[str, int] # {"1": 300}, key = server id, value = item cost on this server
    max_count: int
    purchases: int
    available_on_servers: list
    count_per_one_cost: int # Сколько блоков за одну стоимость

    class Config:
        orm_mode = True


class BuyShopItem(BaseModel):
    block_id: int
    count: int
    server_id: int
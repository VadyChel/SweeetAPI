import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import ShopItemInResponse, BuyShopItem
from swa.core.utils.response_exception import ResponseException
from swa.models import Shop


class ShopCRUD(BaseCRUD[Shop]):
    def get(self, db: Session, skip: int = 0, limit: int = 20) -> typing.List[ShopItemInResponse]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_item(self, db: Session, block_id: id) -> ShopItemInResponse:
        found_item = db.query(self.model).filter(self.model.id == block_id).first()
        if found_item is None:
            raise ResponseException(code=10005)

        return found_item


shop = ShopCRUD(Shop)
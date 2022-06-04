import typing

from . import BaseCRUD
from sqlalchemy import func
from sqlalchemy.orm import Session
from swa.schemas import UserPurchaseInResponse, UserPurchaseInRequest
from swa.models import UsersPurchases


class PurchasesCRUD(BaseCRUD[UsersPurchases]):
    def get_user_purchases(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 20
    ) -> typing.List[UserPurchaseInResponse]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def get_all(
            self, db: Session, skip: int = 0, limit: int = 20
    ) -> typing.List[UserPurchaseInResponse]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_user_purchases_count(self, db: Session, user_id: str) -> int:
        return db.query(self.model).filter(self.model.user_id == user_id).count()

    def get_block_purchases_count(self, db: Session, block_id: int) -> int:
        return db.query(func.count(self.model.id)).filter(
            self.model.bought_item_id == block_id
        ).first()[0]

    def create(self, db: Session, purchase: UserPurchaseInRequest):
        db_purchase = self.model(**purchase.dict())
        db.add(db_purchase)
        db.commit()
        db.refresh(db_purchase)
        return db_purchase
    

purchases = PurchasesCRUD(UsersPurchases)
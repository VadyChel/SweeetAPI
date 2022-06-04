import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import BoughtItemInResponse, BoughtItemInRequest
from swa.core.utils.response_exception import ResponseException
from swa.models import BoughtItems


class BoughtItemsCRUD(BaseCRUD[BoughtItems]):
    def get(self, db: Session, user_id: str) -> typing.List[BoughtItemInResponse]:
        return db.query(self.model).filter(self.model.user_id == user_id).all()

    def create(self, db: Session, block: BoughtItemInRequest):
        db_item = self.model(**block.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item


bought_items = BoughtItemsCRUD(BoughtItems)
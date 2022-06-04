import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import BloksyBalance, BloksyBalanceInTop
from swa.core.utils.response_exception import ResponseException
from swa.models import BloksyBalance


class BloksyBalanceCRUD(BaseCRUD[BloksyBalance]):
    def get_user_balances(self, db: Session, user_id: str) -> typing.List[BloksyBalance]:
        return db.query(self.model).filter(self.model.user_id == user_id).all()

    def get_user_balance_on_server(self, db: Session, user_id: str, server_id: int) -> BloksyBalance:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.server_id == server_id
        ).first()

    def get_rating_on_server(self, db: Session, server_id: int) -> typing.List[BloksyBalance]:
        return db.query(self.model) .filter(self.model.server_id == server_id).order_by(
            desc(self.model.bloksy)
        ).limit(100).all()

    def update(
            self, db: Session, server_id: int, user_id: str, added_bloksy: int
    ) -> None:
        balance_query = db.query(self.model).filter(
            self.model.server_id == server_id,
            self.model.user_id == user_id
        )
        old_balance = balance_query.first()
        if old_balance is None:
            add_bloksy_balance(db=db, user_id=user_id, server_id=server_id, bloksy=added_bloksy)
        else:
            balance_query.update({'bloksy': old_balance.bloksy + added_bloksy})
            db.commit()

    def create(
            self, db: Session, user_id: str, server_id: int, bloksy: int = 0
    ) -> BloksyBalance:
        db_bloksy = self.model(user_id=user_id, server_id=server_id, bloksy=bloksy)
        db.add(db_bloksy)
        db.commit()
        db.refresh(db_bloksy)
        return db_bloksy


bloksy_balances = BloksyBalanceCRUD(BloksyBalance)
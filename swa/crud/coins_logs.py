import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import CoinsLogsInResponse, CoinsLogsInRequest
from swa.core.utils.response_exception import ResponseException
from swa.models import CoinsLogs


class CoinsLogsCRUD(BaseCRUD[CoinsLogs]):
    def get_by_user(
            self,
            db: Session,
            user_id: str,
            skip: int = 0,
            limit: int = 20
    ) -> typing.List[CoinsLogsInResponse]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()

    def get_all(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 20
    ) -> typing.List[CoinsLogsInResponse]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, to_create: CoinsLogsInRequest):
        db_log = self.model(**to_create.dict())
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        return db_log


coins_logs = CoinsLogsCRUD(CoinsLogs)
import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import ServerInResponse
from swa.core.utils.response_exception import ResponseException
from swa.models import Servers


class ServersCRUD(BaseCRUD[Servers]):
    def get(self, db: Session, server_id: int) -> ServerInResponse:
        found_server = db.query(self.model).filter(self.model.id == server_id).first()
        if found_server is None:
            raise ResponseException(code=10001)

        return found_server

    def get_all(self, db: Session, skip: int = 0, limit: int = 20) -> typing.List[ServerInResponse]:
        return db.query(self.model).offset(skip).limit(limit).all()


servers = ServersCRUD(Servers)
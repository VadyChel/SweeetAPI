import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from sqlalchemy import desc
from swa import schemas
from swa.core.utils.response_exception import ResponseException
from swa.models import ServersStat


class ServersStatCRUD(BaseCRUD[ServersStat]):
    def get(self, db: Session, server_id: int) -> typing.Optional[schemas.ServerStats]:
        db_stats = (
            db.query(self.model)
                .filter(self.model.server_id == server_id)
                .order_by(desc(self.model.time))
                .first()
        )
        if db_stats is None:
            return

        record_online = db.query(self.model).filter(
            self.model.server_id == server_id
        ).order_by(desc(self.model.online)).first()
        return schemas.ServerStats(**db_stats.__dict__, record_online=record_online.online)


servers_stat = ServersStatCRUD(ServersStat)

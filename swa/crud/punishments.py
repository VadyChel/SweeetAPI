import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import Punishment
from swa.models import Punishments


class PunishmentsCRUD(BaseCRUD[Punishments]):
    def get_mutelist(self, db: Session, skip: int = 0, limit: int = 20) -> typing.List[Punishment]:
        return db.query(self.model).filter(self.model.type == 'mute').offset(skip).limit(limit).all()

    def get_banlist(self, db: Session, skip: int = 0, limit: int = 20) -> typing.List[Punishment]:
        return db.query(self.model).filter(self.model.type == 'ban').offset(skip).limit(limit).all()

    def get_user_punishments(
            self, db: Session, user_id: str, skip: int = 0, limit: int = 20
    ) -> typing.List[Punishment]:
        return db.query(self.model).filter(self.model.user_id == user_id).offset(skip).limit(limit).all()


punishments = PunishmentsCRUD(Punishments)
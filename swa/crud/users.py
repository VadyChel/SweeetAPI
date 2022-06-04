import datetime

from sqlalchemy.orm import Session
from . import BaseCRUD
from swa.schemas import UserInResponse
from swa.core.utils.response_exception import ResponseException
from swa.models import Users


class UsersCRUD(BaseCRUD[Users]):
    def get(self, db: Session, user_id: str) -> UserInResponse:
        found_user = db.query(self.model).filter(self.model.id == user_id).first()
        if found_user is None:
            raise ResponseException(code=10000)

        return found_user

    def update(
            self,
            db: Session,
            user_id: str,
            updated_fields: dict
    ) -> UserInResponse:
        db.query(self.model).filter(self.model.id == user_id).update(updated_fields)
        db.commit()
        return self.get(db=db, user_id=user_id)

    def create(self, db: Session, user_id: str, nick: str, email: str, coins: int, access_level: int):
        db_user = self.model(
            id=user_id,
            nick=nick,
            email=email,
            coins=coins,
            access_level=access_level,
            created_at=datetime.datetime.now()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


users = UsersCRUD(Users)
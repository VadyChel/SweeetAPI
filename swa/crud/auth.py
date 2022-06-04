from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import AuthInRequest
from swa.core.utils.response_exception import ResponseException
from swa.models import Auth


class AuthCRUD(BaseCRUD[Auth]):
    def check_if_user_registered(self, db: Session, email) -> None:
        if db.query(self.model).filter(self.model.email == email).first() is not None:
            raise ResponseException(code=10007)

    def create(self, db: Session, auth: AuthInRequest, password_hash: str, user_id: str) -> None:
        db_auth = self.model(
            user_id=user_id,
            password_hash=password_hash,
            nick=auth.nick,
            email=auth.email
        )
        db.add(db_auth)
        db.commit()
        db.refresh(db_auth)

    def update(self, db: Session, user_id: str, updated_fields: dict) -> None:
        db.query(self.model).filter(self.model.user_id == user_id).update(updated_fields)
        db.commit()


auth = AuthCRUD(Auth)
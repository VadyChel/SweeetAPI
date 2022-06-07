from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import AuthInRequest, AuthInResponse
from swa.core.utils.response_exception import ResponseException
from swa.models import Auth


class AuthCRUD(BaseCRUD[Auth]):
    def check_if_user_registered(self, db: Session, email) -> None:
        if self.get(db=db, email=email) is not None:
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

    def get(self, db: Session, email: str) -> AuthInResponse:
        return db.query(self.model).filter(self.model.email == email).first()


auth = AuthCRUD(Auth)
from sqlalchemy.orm import Session

from swa import crud
from swa.core.utils.response_exception import ResponseException
from swa.database import SessionLocal
from fastapi import Header, Depends, HTTPException
from swa.core.utils.auth import validate_access_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Authorization:
    def __init__(self, authorization: str = Header(None), db: Session = Depends(get_db)):
        self._raw_authorization = authorization
        self.access_token = None
        self.user_id = None
        self.access_level = None
        self._db = db
        self.current_user = None

        self._validate()

    def _validate(self):
        if self._raw_authorization is None:
            raise HTTPException(status_code=401, detail="Not authorized")

        token_type, _, access_token = self._raw_authorization.partition(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Not authorized")

        token_data = validate_access_token(access_token)
        if token_data is None:
            raise HTTPException(status_code=401, detail="Not authorized")

        db_user = crud.get_user(db=self._db, user_id=token_data["user_id"])

        self.access_token = access_token
        self.db_user = db_user
        self.user_id = token_data["user_id"]
        self.access_level = token_data["access_level"]
        return token_data

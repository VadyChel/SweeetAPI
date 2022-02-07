from swa.database import SessionLocal
from fastapi import Header
from swa.core.utils.auth import get_authorization_params


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authorization_header(authorization: str = Header(None)):
    return get_authorization_params(authorization)
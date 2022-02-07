import time
import os
import base64

from fastapi import HTTPException

from swa import models
from random import randint
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet


def generate_user_id(db: Session):
    return str(int(bin(int(time.time()))+bin(db.query(models.Users).count())[2:]+bin(randint(0, 1000000))[2:], 2))


def generate_token(user_id: str, password_hash: str):
    cipher = Fernet(key=base64.urlsafe_b64encode(os.urandom(32)))
    key = f"{base64.urlsafe_b64encode(os.urandom(64))}{user_id}{password_hash}{time.time()}".encode()
    return cipher.encrypt(key).decode('utf8')


def get_authorization_params(authorization: str) -> str:
    if authorization is None:
        raise HTTPException(status_code=401, detail="Not authorized")

    token_type, _, params = authorization.partition(" ")
    if token_type.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Not authorized")

    return params.strip()

import time
import typing
import jwt
import aiohttp

from datetime import datetime, timedelta
from random import randint
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from swa import models
from swa.core import Config
from swa.core.utils.response_exception import ResponseException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_user_id(db: Session):
    return str(int(bin(int(time.time()))+bin(db.query(models.Users).count())[2:]+bin(randint(0, 1000000))[2:], 2))


def generate_tokens(user_id: str, access_level: int):
    access_token_expires_in = (60 * 60 * 24 * 5)  # 5 days
    refresh_token_expires_in = (60 * 60 * 24 * 45)  # 45 days
    refresh_token = jwt.encode(
        {
            "user_id": user_id,
            "access_level": access_level,
            "exp": int(access_token_expires_in + time.time())
        },
        Config.JWT_REFRESH_SECRET,
        algorithm='HS256'
    )
    access_token = jwt.encode(
        {
            "user_id": user_id,
            "access_level": access_level,
            "exp": int(refresh_token_expires_in + time.time())
        },
        Config.JWT_ACCESS_SECRET,
        algorithm='HS256'
    )
    return {
        "refresh_token": refresh_token,
        "access_token": access_token,
        "expires_in": access_token_expires_in
    }


def validate_access_token(access_token: str) -> typing.Optional[dict]:
    try:
        return jwt.decode(
            access_token,
            Config.JWT_ACCESS_SECRET,
            algorithms=["HS256"],
            options={"verify_signature": True}
        )
    except jwt.PyJWTError:
        return


def validate_refresh_token(refresh_token: str) -> typing.Optional[dict]:
    try:
        return jwt.decode(
            refresh_token,
            Config.JWT_REFRESH_SECRET,
            algorithms=["HS256"],
            options={"verify_signature": True}
        )
    except jwt.PyJWTError:
        return


async def validate_recaptcha_token(token: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://www.google.com/recaptcha/api/siteverify",
                params={
                    "response": token,
                    "secret": Config.G_RECAPTCHA_SECRET
                }
        ) as resp:
            success = await resp.json()
            if not success:
                raise ResponseException(code=10011)

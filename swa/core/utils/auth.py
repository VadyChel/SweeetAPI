import time
import typing
import jwt
import aiohttp

from datetime import datetime, timedelta
from random import randint
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.config import Config as SConfig
from authlib.integrations.starlette_client import OAuth

from swa import models
from swa.schemas import GoogleAuthInRequest
from swa.core import Config
from swa.core.utils.response_exception import ResponseException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
config_data = {
    'GOOGLE_CLIENT_ID': Config.GOOGLE_CLIENT_ID,
    'GOOGLE_CLIENT_SECRET': Config.GOOGLE_CLIENT_SECRET
}
starlette_config = SConfig(environ=config_data)
oauth = OAuth(config=starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)
oauth_cache = {}


async def create_google_auth_url(redirect_uri: str):
    authorization_url = await oauth.google.create_authorization_url(redirect_uri)
    key = authorization_url.pop('state')
    authorization_url['redirect_uri'] = redirect_uri
    oauth_cache[key] = {'data': authorization_url, 'exp': time.time()+(60*60)}
    return RedirectResponse(authorization_url['url'], status_code=302)


async def get_google_userinfo(auth: GoogleAuthInRequest):
    if auth.error is not None:
        raise HTTPException(status_code=401, detail=f'{auth.error}: {auth.error_description}')

    cache_value = oauth_cache.get(auth.state)
    state_data = cache_value.get('data') if cache_value else None
    if state_data is None:
        raise HTTPException(status_code=401, detail='State in request not equal state in response')

    # Clear expired keys in cache
    now = time.time()
    for key in dict(oauth_cache):
        value = oauth_cache[key]
        exp = value.get('exp')
        if not exp or exp < now:
            oauth_cache.pop(key)

    access_token = await oauth.google.fetch_access_token(
        code=auth.code,
        state=auth.state,
        redirect_uri=state_data['redirect_uri']
    )

    # Get userinfo of google account
    return await oauth.google.parse_id_token(access_token, nonce=state_data['nonce'])


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
                    "secret": Config.RECAPTCHA_SECRET
                }
        ) as resp:
            success = await resp.json()
            if not success:
                raise ResponseException(code=10011)

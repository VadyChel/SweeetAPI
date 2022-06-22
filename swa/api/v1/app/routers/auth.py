import typing
import time

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Cookie, HTTPException, Response, Request
from fastapi.responses import JSONResponse, RedirectResponse

from swa.core.utils.auth import (
    validate_recaptcha_token,
    generate_user_id,
    generate_tokens,
    get_google_userinfo,
    create_google_auth_url
)
from swa.core.utils.response_exception import ResponseException
from swa.core.utils.other import model_to_dict, fix_datetime, create_auth_response
from swa.core import Config
from swa.api.v1.app import dependencies
from swa import schemas, crud
from swa.auth import DefaultStrategy, GoogleStrategy


router = APIRouter()
strategies = {
    'google': GoogleStrategy(),
    'default': DefaultStrategy()
}


@router.get('/google/url')
async def google_login(redirect_uri: str):
    return await create_google_auth_url(redirect_uri)


@router.post("/register", response_model=schemas.TokenInResponse)
async def get_token_and_register(auth: schemas.AuthInRequest, db: Session = Depends(dependencies.get_db)):
    await validate_recaptcha_token(auth.g_recaptcha_response)

    return create_auth_response(strategies.get('default').register(db=db, info=auth))


@router.post("/login", response_model=schemas.TokenInResponse)
async def get_token(
        auth: typing.Union[schemas.LoginInRequest, schemas.GoogleAuthInRequest],
        strategy: str = 'google',
        db: Session = Depends(dependencies.get_db)
):
    return create_auth_response(strategies.get(strategy).authorize(
        db=db, info=await get_google_userinfo(auth) if strategy == 'google' else auth
    ))


@router.post("/revoke")
async def revoke_token(
        response: Response,
        refresh_token_cookie: str = Cookie(default=None, alias="refresh_token"),
        db: Session = Depends(dependencies.get_db)
):
    if refresh_token_cookie is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    response.delete_cookie("refresh_token", httponly=True)
    return crud.auth_tokens.revoke_token(db=db, refresh_token=refresh_token_cookie)


@router.get("/refresh", response_model=schemas.TokenInResponse)
async def refresh_token(
        refresh_token_cookie: str = Cookie(default=None, alias="refresh_token"),
        db: Session = Depends(dependencies.get_db)
):
    if refresh_token_cookie is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return create_auth_response(crud.auth_tokens.get_refresh_token(
        db=db,
        refresh_token=refresh_token_cookie
    ))

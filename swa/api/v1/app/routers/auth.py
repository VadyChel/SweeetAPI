from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Cookie, HTTPException, Response
from fastapi.responses import JSONResponse

from swa.core.utils.response_exception import ResponseException
from swa.core.utils.other import model_to_dict, fix_datetime
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.post("/register", response_model=schemas.TokenInResponse)
async def get_token_and_register(auth: schemas.AuthInRequest, db: Session = Depends(dependencies.get_db)):
    token = fix_datetime(crud.register(db=db, auth=auth).dict())
    response = JSONResponse(content=token)
    response.set_cookie(
        key="refresh_token",
        value=token["refresh_token"],
        max_age=token["expiry_at"],
        httponly=True
    )
    return response


@router.post("/login", response_model=schemas.TokenInResponse)
async def get_token(auth: schemas.LoginInRequest,  db: Session = Depends(dependencies.get_db)):
    token = fix_datetime(crud.authorize(db=db, auth=auth).dict())
    response = JSONResponse(content=token)
    response.set_cookie(
        key="refresh_token",
        value=token["refresh_token"],
        max_age=token["expiry_at"],
        httponly=True
    )
    return response


@router.post("/revoke")
async def revoke_token(
        response: Response,
        refresh_token_cookie: str = Cookie(default=None, alias="refresh_token"),
        db: Session = Depends(dependencies.get_db)
):
    if refresh_token_cookie is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    response.delete_cookie("refresh_token", httponly=True)
    return crud.revoke_token(db=db, refresh_token=refresh_token_cookie)


@router.get("/refresh", response_model=schemas.TokenInResponse)
async def refresh_token(
        refresh_token_cookie: str = Cookie(default=None, alias="refresh_token"),
        db: Session = Depends(dependencies.get_db)
):
    if refresh_token_cookie is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    refreshed_token = fix_datetime(crud.get_refresh_token(
        db=db,
        refresh_token=refresh_token_cookie
    ).dict())
    response = JSONResponse(content=refreshed_token)
    response.set_cookie(
        key="refresh_token",
        value=refreshed_token["refresh_token"],
        max_age=refreshed_token["expiry_at"],
        httponly=True
    )
    return response

import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.post(
    "/register",
    response_model=schemas.TokenInResponse
)
async def get_token_and_register(auth: schemas.AuthInRequest, db: Session = Depends(dependencies.get_db)):
    return crud.register(db=db, auth=auth)


@router.post(
    "/token",
    response_model=schemas.TokenInResponse
)
async def get_token(auth: schemas.AuthInRequest, db: Session = Depends(dependencies.get_db)):
    return crud.authorize(db=db, user_id=crud.get_user_id_by_auth(db=db, auth=auth))


@router.post("/revoke")
async def revoke_token(
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    token, _, user_id = authorization.partition(" ")
    token, user_id = token.strip(), user_id.strip()
    if not user_id.isdigit():
        raise HTTPException(status_code=400, detail="An invalid user id was provided")

    return crud.revoke_token(db=db, token=token, user_id=user_id)


@router.post(
    "/refresh",
    response_model=schemas.TokenInResponse
)
async def refresh_token(
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    return crud.get_refresh_token(db=db, refresh_token=authorization)

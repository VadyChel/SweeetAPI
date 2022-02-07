from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserInResponse
)
async def get_user(user_id: str, db: Session = Depends(dependencies.get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    return user


@router.get(
    "/users/@me",
    response_model=schemas.UserInResponse
)
async def get_user_by_token(
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10000, detail='Invalid authorization')

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    return user


@router.put(
    "/users/@me/nick",
    response_model=schemas.UserInResponse
)
async def change_user_nick(
        new_nick: schemas.UserNickInRequest,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10000, detail='Invalid authorization')

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    crud.edit_auth(db=db, user_id=user_id, updated_fields={'nick': new_nick.new_nick})
    return crud.edit_user(db=db, user_id=user_id, updated_fields={'nick': new_nick.new_nick})


@router.put(
    "/users/{user_id}/nick",
    response_model=schemas.UserInResponse
)
async def change_user_nick_by_id(
        user_id: str,
        new_nick: schemas.UserNickInRequest,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    current_user_id = crud.get_current_user_id(db=db, token=authorization)
    if current_user_id is None:
        raise ResponseException(code=10000, detail='Invalid authorization')

    current_user = crud.get_user(db=db, user_id=current_user_id)
    if current_user is None:
        raise ResponseException(code=10000, detail="User not found")

    if current_user.access_level < 22:
        raise ResponseException(code=10000, detail="You don't have permissions")

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    crud.edit_auth(db=db, user_id=user_id, updated_fields={'nick': new_nick.new_nick})
    return crud.edit_user(db=db, user_id=user_id, updated_fields={'nick': new_nick.new_nick})
import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud
from swa.core.config import Config


router = APIRouter()


@router.get(
    "/users/@me",
    response_model=schemas.UserInResponse
)
async def get_current_user(
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10003)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    return user


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserInResponse
)
async def get_user(user_id: str, db: Session = Depends(dependencies.get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    return user


@router.get(
    "/users/@me/balance",
    response_model=typing.List[schemas.BloksyBalance]
)
async def get_user_balance_by_token(
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10003)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    return crud.get_user_balance(db=db, user_id=user_id)


@router.get(
    "/users/@me/balance/{server_id}",
    response_model=schemas.BloksyBalance
)
async def get_user_balance_on_server_by_token(
        server_id: int,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10003)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    return crud.get_user_balance_on_server(db=db, user_id=user_id, server_id=server_id)


@router.get(
    "/users/{user_id}/balance",
    response_model=typing.List[schemas.BloksyBalance]
)
async def get_user_balance_by_token(
        user_id: str,
        db: Session = Depends(dependencies.get_db)
):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    return crud.get_user_balance(db=db, user_id=user_id)


@router.get(
    "/users/{user_id}/balance/{server_id}",
    response_model=schemas.BloksyBalance
)
async def get_user_balance_on_server_by_token(
        user_id: str,
        server_id: int,
        db: Session = Depends(dependencies.get_db)
):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    return crud.get_user_balance_on_server(db=db, user_id=user_id, server_id=server_id)


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
        raise ResponseException(code=10003)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

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
        raise ResponseException(code=10003)

    current_user = crud.get_user(db=db, user_id=current_user_id)
    if current_user is None:
        raise ResponseException(code=10000)

    if current_user.access_level < 22:
        raise ResponseException(code=10004)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    crud.edit_auth(db=db, user_id=user_id, updated_fields={'nick': new_nick.new_nick})
    return crud.edit_user(db=db, user_id=user_id, updated_fields={'nick': new_nick.new_nick})


@router.get(
    "/users/@me/inventory",
    response_model=typing.List[schemas.BoughtItemInResponse]
)
async def get_user_bought_items(
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10003)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    return crud.get_user_bought_items(db=db, user_id=user_id)


@router.post(
    "/users/@me/exchange",
    response_model=schemas.UserInResponse
)
async def exchange_user_money_to_bloksy(
        coins: int,
        server_id: int,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10003)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    if user.coins < coins:
        raise ResponseException(code=10006)

    crud.change_bloksy_balance(
        db=db,
        server_id=server_id,
        user_id=user_id,
        added_bloksy=Config.COINS_EXCHANGE_FUNC(coins)
    )
    return crud.edit_user(db=db, user_id=user_id, updated_fields={'coins': user.coins-coins})

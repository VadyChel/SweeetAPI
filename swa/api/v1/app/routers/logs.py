import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/logs/coins",
    response_model=typing.List[schemas.CoinsLogsInResponse]
)
async def get_all_coins_logs(
        limit: int = 20,
        skip: int = 0,
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    if current_user.access_level < 2:
        raise ResponseException(code=10004)

    return crud.coins_logs.get_all(db=db, limit=limit, skip=skip)


@router.get(
    "/logs/coins/users/{user_id}",
    response_model=typing.List[schemas.CoinsLogsInResponse]
)
async def get_coins_logs(
        user_id: str,
        limit: int = 20,
        skip: int = 0,
        db: Session = Depends(dependencies.get_db)
):
    crud.users.get(db=db, user_id=user_id)  # Check if user not found
    return crud.coins_logs.get_by_user(db=db, user_id=user_id, limit=limit, skip=skip)


@router.get(
    "/logs/coins/@me",
    response_model=typing.List[schemas.CoinsLogsInResponse]
)
async def get_coins_logs_by_token(
        limit: int = 20,
        skip: int = 0,
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    return crud.coins_logs.get_by_user(db=db, user_id=current_user.user_id, limit=limit, skip=skip)


@router.get(
    "/logs/purchases",
    response_model=typing.List[schemas.UserPurchaseInResponse]
)
async def get_all_purchases(
        limit: int = 20,
        skip: int = 0,
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    if current_user.access_level < 2:
        raise ResponseException(code=10004)

    return crud.purchases.get_all(db=db, limit=limit, skip=skip)


@router.get(
    "/logs/purchases/users/{user_id}",
    response_model=typing.List[schemas.UserPurchaseInResponse]
)
async def get_user_purchases(
        user_id: str,
        limit: int = 20,
        skip: int = 0,
        db: Session = Depends(dependencies.get_db)
):
    crud.users.get(db=db, user_id=user_id)  # Check if user not found
    return crud.purchases.get_user_purchases(db=db, user_id=user_id, limit=limit, skip=skip)


@router.get(
    "/logs/purchases/@me",
    response_model=typing.List[schemas.UserPurchaseInResponse]
)
async def get_user_purchases_by_token(
        limit: int = 20,
        skip: int = 0,
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    return crud.purchases.get_user_purchases(db=db, user_id=current_user.user_id, limit=limit, skip=skip)


@router.get(
    "/logs/purchases/users/{user_id}/count",
    response_model=int
)
async def get_user_purchases_count(user_id: str, db: Session = Depends(dependencies.get_db)):
    return crud.purchases.get_user_purchases_count(db=db, user_id=user_id)


@router.get(
    "/logs/purchases/@me/count",
    response_model=int
)
async def get_user_purchases_by_token(
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    return crud.purchases.get_user_purchases_count(db=db, user_id=current_user.user_id)


@router.get(
    "/logs/purchases/blocks/{block_id}/count",
    response_model=int
)
async def get_block_purchases_count(block_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.purchases.get_block_purchases_count(db=db, block_id=block_id)

import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/purchases/users/{user_id}",
    response_model=typing.List[schemas.UserPurchaseInResponse]
)
async def get_user_purchases(
        user_id: int,
        limit: int = 20,
        skip: int = 0,
        db: Session = Depends(dependencies.get_db)
):
    return crud.get_user_purchases(db=db, user_id=user_id, limit=limit, skip=skip)


@router.get(
    "/purchases/blocks/{block_id}",
    response_model=typing.List[schemas.BlockPurchaseInResponse]
)
async def get_block_purchases(
        block_id: int,
        limit: int = 20,
        skip: int = 0,
        db: Session = Depends(dependencies.get_db)
):
    return crud.get_block_purchases(db=db, block_id=block_id, limit=limit, skip=skip)


@router.get(
    "/purchases/users/{user_id}/count",
    response_model=int
)
async def get_user_purchases_count(user_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.get_user_purchases_count(db=db, user_id=user_id)


@router.get(
    "/purchases/blocks/{block_id}/count",
    response_model=int
)
async def get_block_purchases_count(block_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.get_block_purchases_count(db=db, block_id=block_id)


@router.get(
    "/purchases/blocks/{block_id}/summarycount",
    response_model=int
)
async def get_block_purchases_summmary_count(block_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.get_block_purchases_summary_count(db=db, block_id=block_id)["count"]

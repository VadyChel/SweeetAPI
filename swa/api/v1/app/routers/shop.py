import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/shop",
    response_model=typing.List[schemas.ShopItemInResponse]
)
async def get_shop(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.get_shop(db=db, skip=skip, limit=limit)


@router.post(
    "/shop/buy/",
    response_model=schemas.NewsInResponse
)
async def buy_block(
        buying_data: schemas.BuyShopItem,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10000, detail="Invalid authorization")

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    block = crud.get_shop_item(db=db, block_id=buying_data.block_id)
    if block is None:
        raise ResponseException(code=10000, detail="Block not found")

    cost = block.cost * buying_data.count/block.count_per_one_cost
    if user.bloksy < cost:
        raise ResponseException(code=10000, detail='There is not enough coins in user balance')

    return crud.edit_user(db=db, user_id=user_id, updated_fields={'coins': user.bloksy-cost})
import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.managers import QueueItemSchema, purchases_manager
from swa.core.utils.other import model_to_dict
from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/shop",
    response_model=typing.List[schemas.ShopItemInResponse]
)
async def get_shop(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return [
        {
            "purchases": crud.get_block_purchases_count(db=db, block_id=shop_item.id),
            **model_to_dict(shop_item)
        }
        for shop_item in crud.get_shop(db=db, skip=skip, limit=limit)
    ]


@router.post(
    "/shop/buy/",
    response_model=schemas.UserInResponse
)
async def buy_block(
        buying_data: schemas.BuyShopItem,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10003)

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000)

    block = crud.get_shop_item(db=db, block_id=buying_data.block_id)
    if block is None:
        raise ResponseException(code=10005)

    cost = block.cost[str(buying_data.server_id)] * (buying_data.count / block.count_per_one_cost)
    if user.coins < cost:
        raise ResponseException(code=10006)

    purchases_manager.add_item(QueueItemSchema(
        db=db,
        data={
            "type": "user",
            "purchase": schemas.UserPurchaseInRequest(
                user_id=user_id,
                cost=cost,
                bought_item=block.block_name,
                count=buying_data.count,
                bought_item_id=block.id,
                type='block'
            )
        }
    ))
    crud.add_user_bought_items(
        db=db,
        block=schemas.BoughtItemInRequest(
            minecraft_item_id=block.minecraft_block_id,
            item_id=block.id,
            count=buying_data.count,
            item_name=block.block_name,
            user_id=user_id
        ),
    )
    return crud.edit_user(db=db, user_id=user_id, updated_fields={'coins': user.coins-cost})
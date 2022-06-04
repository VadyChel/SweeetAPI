import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.other import model_to_dict
from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/servers",
    response_model=typing.List[schemas.ServerInResponse]
)
async def get_servers(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.servers.get_all(db=db, skip=skip, limit=limit)


@router.get(
    "/servers/{server_id}",
    response_model=schemas.ServerInResponse
)
async def get_server(server_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.servers.get(db=db, server_id=server_id)


@router.get(
    "/servers/{server_id}/stats",
    response_model=schemas.ServerStats
)
async def get_server_stats(server_id: int, db: Session = Depends(dependencies.get_db)):
    crud.servers.get(db=db, server_id=server_id)  # Check if server exists
    return crud.servers_stat.get(db=db, server_id=server_id)


@router.get(
    "/servers/{server_id}/rating",
    response_model=typing.List[schemas.BloksyBalanceInTop]
)
async def get_server_top_balances(server_id: int, db: Session = Depends(dependencies.get_db)):
    return [
        {
            **model_to_dict(balance),
            "user_nick": crud.users.get(db=db, user_id=balance.user_id).nick,
        }
        for balance in crud.bloksy_balances.get_rating_on_server(db=db, server_id=server_id)
    ]

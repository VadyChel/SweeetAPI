import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/mutelist",
    response_model=typing.List[schemas.ServerInResponse]
)
async def get_mutelist(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.get_servers(db=db, skip=skip, limit=limit)


@router.get(
    "/banlist",
    response_model=schemas.ServerInResponse
)
async def get_banlist(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    server = crud.get_server(db=db, server_id=server_id)
    if server is None:
        raise ResponseException(code=10002, detail="Bot not found")

    return server

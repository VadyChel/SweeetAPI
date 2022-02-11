import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/servers",
    response_model=typing.List[schemas.ServerInResponse]
)
async def get_servers(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.get_servers(db=db, skip=skip, limit=limit)


@router.get(
    "/servers/{server_id}",
    response_model=schemas.ServerInResponse
)
async def get_server(server_id: int, db: Session = Depends(dependencies.get_db)):
    server = crud.get_server(db=db, server_id=server_id)
    if server is None:
        raise ResponseException(code=10001)

    return server


@router.get(
    "/servers/{server_id}/stats",
    response_model=schemas.ServerStats
)
async def get_server_stats(server_id: int, db: Session = Depends(dependencies.get_db)):
    if crud.get_server(db=db, server_id=server_id) is None:
        raise ResponseException(code=10001)

    return crud.get_server_stats(db=db, server_id=server_id)

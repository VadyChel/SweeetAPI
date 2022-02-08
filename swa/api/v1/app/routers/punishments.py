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
    return crud.get_mutelist(db=db, skip=skip, limit=limit)


@router.get(
    "/banlist",
    response_model=schemas.ServerInResponse
)
async def get_banlist(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.get_banlist(db=db, skip=skip, limit=limit)

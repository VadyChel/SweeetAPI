import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/mutelist",
    response_model=typing.List[schemas.Punishment]
)
async def get_mutelist(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.punishments.get_mutelist(db=db, skip=skip, limit=limit)


@router.get(
    "/banlist",
    response_model=typing.List[schemas.Punishment]
)
async def get_banlist(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.punishments.get_banlist(db=db, skip=skip, limit=limit)


@router.get(
    "/punishments/{user_id}",
    response_model=typing.List[schemas.Punishment]
)
async def get_user_punishments(
        user_id: str,
        skip: int = 0,
        limit: int = 20,
        db: Session = Depends(dependencies.get_db)
):
    return crud.punishments.get_user_punishments(db=db, user_id=user_id, skip=skip, limit=limit)

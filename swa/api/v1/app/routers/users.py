from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/users/{user_id}",
    response_model=schemas.UserInResponse
)
async def get_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10002, detail="Bot not found")

    return user

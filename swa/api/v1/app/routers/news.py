import typing

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from swa.core.utils.response_exception import ResponseException
from swa.api.v1.app import dependencies
from swa import schemas, crud


router = APIRouter()


@router.get(
    "/news",
    response_model=typing.List[schemas.NewsInResponse]
)
async def get_all_news(skip: int = 0, limit: int = 20, db: Session = Depends(dependencies.get_db)):
    return crud.get_all_news(db=db, skip=skip, limit=limit)


@router.get(
    "/news/{news_id}",
    response_model=schemas.NewsInResponse
)
async def get_news(news_id: int, db: Session = Depends(dependencies.get_db)):
    news = crud.get_news(db=db, news_id=news_id)
    if news is None:
        raise ResponseException(code=10000, detail="News not found")

    return news


@router.post(
    "/news",
    response_model=schemas.NewsInResponse
)
async def create_news(
        news: schemas.NewsInRequest,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10000, detail="Invalid authorization")

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    if user.access_level < 1:
        raise ResponseException(code=10000, detail="You don't have permissions")

    news.author_id = user_id
    return crud.add_news(db=db, news=news)


@router.patch(
    "/news/{news_id}",
    response_model=schemas.NewsInResponse
)
async def edit_news(
        news_id: int,
        news_changes: schemas.NewsInRequestEdit,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10000, detail="Invalid authorization")

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    news = crud.get_news(db=db, news_id=news_id)
    if news is None:
        raise ResponseException(code=10002, detail="Bot not found")

    if user.access_level < 1 or news.author_id != news.author_id:
        raise ResponseException(code=10000, detail="You don't have permissions")

    return crud.edit_news(db=db, news_id=news_id, news=news_changes)


@router.delete(
    "/news/{news_id}",
    response_model=schemas.NewsInResponse
)
async def delete_news(
        news_id: int,
        authorization: str = Depends(dependencies.authorization_header),
        db: Session = Depends(dependencies.get_db)
):
    user_id = crud.get_current_user_id(db=db, token=authorization)
    if user_id is None:
        raise ResponseException(code=10000, detail="Invalid authorization")

    user = crud.get_user(db=db, user_id=user_id)
    if user is None:
        raise ResponseException(code=10000, detail="User not found")

    news = crud.get_news(db=db, news_id=news_id)
    if news is None:
        raise ResponseException(code=10002, detail="Bot not found")

    if user.access_level < 1 or news.author_id != news.author_id:
        raise ResponseException(code=10000, detail="You don't have permissions")

    return crud.delete_news(db=db, news_id=news_id)


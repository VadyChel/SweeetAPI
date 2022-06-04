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
    return crud.news.get_all(db=db, skip=skip, limit=limit)


@router.get(
    "/news/{news_id}",
    response_model=schemas.NewsInResponse
)
async def get_news(news_id: int, db: Session = Depends(dependencies.get_db)):
    return crud.news.get(db=db, news_id=news_id)


@router.post(
    "/news",
    response_model=schemas.NewsInResponse
)
async def create_news(
        news: schemas.NewsInRequest,
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    if current_user.access_level < 1:
        raise ResponseException(code=10004)

    news.author_id = current_user.user_id
    return crud.news.create(db=db, news_to_create=news)


@router.patch(
    "/news/{news_id}",
    response_model=schemas.NewsInResponse
)
async def edit_news(
        news_id: int,
        news_changes: schemas.NewsInRequestEdit,
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    news = crud.news.get(db=db, news_id=news_id)
    if current_user.access_level <= 1 or news.author_id != current_user.user_id:
        raise ResponseException(code=10004)

    return crud.news.update(db=db, news_id=news_id, news_to_edit=news_changes)


@router.delete(
    "/news/{news_id}",
    response_model=schemas.NewsInResponse
)
async def delete_news(
        news_id: int,
        current_user: dependencies.Authorization = Depends(dependencies.Authorization),
        db: Session = Depends(dependencies.get_db)
):
    news = crud.news.get(db=db, news_id=news_id)
    if current_user.access_level <= 1 or news.author_id != current_user.user_id:
        raise ResponseException(code=10004)

    return crud.news.delete(db=db, news_id=news_id)


import typing

from . import BaseCRUD
from sqlalchemy.orm import Session
from swa.schemas import NewsInResponse, NewsInRequest, NewsInRequestEdit
from swa.core.utils.response_exception import ResponseException
from swa.models import News


class NewsCRUD(BaseCRUD[News]):
    def get(self, db: Session, news_id: int) -> NewsInResponse:
        found_news = db.query(self.model).filter(self.model.id == news_id).first()
        if found_news is None:
            raise ResponseException(code=10002)

        return found_news

    def get_all(
            self,
            db: Session,
            skip: int = 0,
            limit: int = 20
    ) -> typing.List[NewsInResponse]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, news_to_create: NewsInRequest):
        db_news = self.model(**news_to_create.dict())
        db.add(db_news)
        db.commit()
        db.refresh(db_news)
        return db_news

    def update(
            self,
            db: Session,
            news_id: int,
            news_to_edit: NewsInRequestEdit
    ) -> NewsInResponse:
        db.query(self.model).filter(self.model.id == news_id).update(
            news_to_edit.dict(exclude_none=True)
        )
        db.commit()
        return self.get(db=db, news_id=news_id)

    def delete(self, db: Session, news_id: int) -> NewsInResponse:
        deleted_news = self.get(db=db, news_id=news_id)
        db.query(self.model).filter(self.model.id == news_id).delete()
        db.commit()
        return deleted_news


news = NewsCRUD(News)
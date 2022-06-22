from abc import ABC
from sqlalchemy.orm import Session


class BaseStrategy(ABC):
    def authorize(self, db: Session, info):
        pass


class LocalStrategy(BaseStrategy):
    def register(self, db: Session, info):
        pass
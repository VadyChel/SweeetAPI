from typing import Generic, Type, TypeVar
from sqlalchemy.orm import Session
from swa.database import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseCRUD(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
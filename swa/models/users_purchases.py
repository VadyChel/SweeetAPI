from sqlalchemy import Column, BIGINT, TIMESTAMP, String, Integer
from ..database import Base


class UsersPurchases(Base):
    __tablename__ = "users_purchases"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    bought_item = Column(String)
    bought_item_id = Column(BIGINT)
    cost = Column(BIGINT)
    time = Column(TIMESTAMP)
    count = Column(Integer)
    type = Column(String)
    remove_time = Column(TIMESTAMP)
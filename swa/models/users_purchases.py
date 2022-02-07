from sqlalchemy import Column, BIGINT, TIMESTAMP, String
from ..database import Base


class UsersPurchases(Base):
    __tablename__ = "users_purchases"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    bought_item = Column(String)
    cost = Column(BIGINT)
    time = Column(TIMESTAMP)
    coins_number = Column(BIGINT)
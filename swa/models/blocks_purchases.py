from sqlalchemy import Column, BIGINT, TIMESTAMP, String
from ..database import Base


class BlocksPurchases(Base):
    __tablename__ = "blocks_purchases"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    block_id = Column(BIGINT)
    block_name = Column(String)
    count = Column(BIGINT)
    time = Column(TIMESTAMP)
    coins_number = Column(BIGINT)
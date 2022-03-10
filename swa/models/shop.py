from sqlalchemy import Column, BIGINT, String, JSON
from ..database import Base


class Shop(Base):
    __tablename__ = "shop"

    id = Column(BIGINT, primary_key=True)
    minecraft_block_id = Column(String)
    block_name = Column(String)
    mod = Column(JSON)
    max_count = Column(BIGINT)
    count_per_one_cost = Column(BIGINT)
    available_on_servers = Column(JSON)
    cost = Column(JSON)
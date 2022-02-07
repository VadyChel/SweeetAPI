from sqlalchemy import Column, BIGINT, JSON, String
from ..database import Base


class DonateItems(Base):
    __tablename__ = "donate_items"

    id = Column(BIGINT, primary_key=True)
    name = Column(String)
    cost = Column(String)
    flags = Column(JSON)
    blocks = Column(JSON)

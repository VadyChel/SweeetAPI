from sqlalchemy import Column, BIGINT, String
from ..database import Base


class BoughtItems(Base):
    __tablename__ = "bought_items"

    id = Column(BIGINT, primary_key=True)
    minecraft_item_id = Column(String)
    count = Column(BIGINT)
    item_id = Column(BIGINT)
    item_name = Column(String)
    user_id = Column(String)
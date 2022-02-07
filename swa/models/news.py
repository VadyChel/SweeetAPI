from sqlalchemy import Column, BIGINT, TIMESTAMP, String
from ..database import Base


class News(Base):
    __tablename__ = "news"

    id = Column(BIGINT, primary_key=True)
    title = Column(String)
    text = Column(String)
    created_at = Column(TIMESTAMP)
    edited_at = Column(TIMESTAMP)
    author_id = Column(String)
    image_url = Column(String)
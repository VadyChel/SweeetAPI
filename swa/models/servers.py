from sqlalchemy import Column, BIGINT, String, JSON
from ..database import Base


class Servers(Base):
    __tablename__ = "servers"

    id = Column(BIGINT, primary_key=True)
    name = Column(String)
    description = Column(String)
    mods = Column(JSON)
    image_url = Column(String)
    info = Column(JSON)
    specials = Column(JSON)
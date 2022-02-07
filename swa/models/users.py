from sqlalchemy import Column, BIGINT, String, SMALLINT
from ..database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    nick = Column(String)
    email = Column(String)
    skin_url = Column(String)
    access_level = Column(SMALLINT)
    coins = Column(BIGINT) # In-game money
    bloksy = Column(BIGINT) # Money to bloksy
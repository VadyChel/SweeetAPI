from sqlalchemy import Column, BIGINT, String, TIMESTAMP
from ..database import Base


class Punishments(Base):
    __tablename__ = "punishments"

    id = Column(BIGINT, primary_key=True)
    nick = Column(String)
    reason = Column(String)
    server = Column(String)
    moderator = Column(String)
    type = Column(String)
    time = Column(TIMESTAMP)
    remove_time = Column(TIMESTAMP)

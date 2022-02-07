from sqlalchemy import Column, BIGINT, String
from ..database import Base


class Auth(Base):
    __tablename__ = "auth"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    email = Column(String)
    nick = Column(String)
    password_hash = Column(String)
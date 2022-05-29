from sqlalchemy import Column, BIGINT, String, JSON
from ..database import Base


class AuthTokens(Base):
    __tablename__ = "auth_tokens"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    refresh_token = Column(String)
    access_level = Column(BIGINT)
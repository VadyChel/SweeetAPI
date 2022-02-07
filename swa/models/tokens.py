from sqlalchemy import Column, BIGINT, String
from ..database import Base


class AuthTokens(Base):
    __tablename__ = "auth_tokens"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    token = Column(String)
    refresh_token = Column(String)
    expiry_at = Column(BIGINT)
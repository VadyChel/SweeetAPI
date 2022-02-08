from sqlalchemy import Column, BIGINT, String
from ..database import Base


class BloksyBalance(Base):
    __tablename__ = "bloksy_balances"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    server_id = Column(BIGINT)
    bloksy = Column(BIGINT)

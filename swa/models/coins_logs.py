from sqlalchemy import Column, BIGINT, String, DATETIME
from ..database import Base


class CoinsLogs(Base):
    __tablename__ = "coins_logs"

    id = Column(BIGINT, primary_key=True)
    user_id = Column(String)
    coins_count = Column(BIGINT)
    reason = Column(String)
    time = Column(DATETIME)
from sqlalchemy import Column, BIGINT
from ..database import Base


class ServersStat(Base):
    __tablename__ = "servers_stats"

    id = Column(BIGINT, primary_key=True)
    server_id = Column(BIGINT)
    online = Column(BIGINT)
    tps = Column(BIGINT)
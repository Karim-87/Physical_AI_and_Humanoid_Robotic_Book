from sqlalchemy import Column, String, Integer, DateTime
from ..config.database import Base
from datetime import datetime
import uuid


class RateLimitRecord(Base):
    __tablename__ = "rate_limit_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    ip_address = Column(String, index=True)  # IP address being rate limited
    request_count = Column(Integer, default=0)  # Number of requests in current window
    window_start = Column(DateTime, default=datetime.utcnow)  # Start of current rate limit window
    expires_at = Column(DateTime)  # When rate limit expires
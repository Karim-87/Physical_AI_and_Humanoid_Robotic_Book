from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.rate_limit import RateLimitRecord
from ..config.settings import settings
from fastapi import HTTPException, status
import hashlib


class RateLimitService:
    def __init__(self):
        self.requests_limit = settings.RATE_LIMIT_REQUESTS
        self.window_seconds = settings.RATE_LIMIT_WINDOW

    def _get_hashed_ip(self, ip_address: str) -> str:
        """Hash the IP address for privacy."""
        return hashlib.sha256(ip_address.encode()).hexdigest()

    def is_allowed(self, db: Session, ip_address: str) -> bool:
        """Check if a request from the given IP is allowed."""
        hashed_ip = self._get_hashed_ip(ip_address)

        # Calculate the window start time
        window_start = datetime.utcnow() - timedelta(seconds=self.window_seconds)

        # Get or create the rate limit record
        record = db.query(RateLimitRecord).filter(
            RateLimitRecord.ip_address == hashed_ip,
            RateLimitRecord.window_start >= window_start
        ).first()

        if not record:
            # Create a new record for this window
            record = RateLimitRecord(
                ip_address=hashed_ip,
                request_count=1,
                window_start=datetime.utcnow(),
                expires_at=datetime.utcnow() + timedelta(seconds=self.window_seconds)
            )
            db.add(record)
            db.commit()
            return True

        # Check if we're still in the same window
        if record.expires_at > datetime.utcnow():
            # If we're still in the same window, check the count
            if record.request_count >= self.requests_limit:
                return False
            else:
                # Increment the count
                record.request_count += 1
                db.commit()
                return True
        else:
            # Create a new window
            record.request_count = 1
            record.window_start = datetime.utcnow()
            record.expires_at = datetime.utcnow() + timedelta(seconds=self.window_seconds)
            db.commit()
            return True

    def get_remaining_requests(self, db: Session, ip_address: str) -> int:
        """Get the number of remaining requests for the given IP."""
        hashed_ip = self._get_hashed_ip(ip_address)

        # Calculate the window start time
        window_start = datetime.utcnow() - timedelta(seconds=self.window_seconds)

        record = db.query(RateLimitRecord).filter(
            RateLimitRecord.ip_address == hashed_ip,
            RateLimitRecord.window_start >= window_start
        ).first()

        if not record or record.expires_at <= datetime.utcnow():
            # No record or current window has expired
            return self.requests_limit

        return max(0, self.requests_limit - record.request_count)

    def get_reset_time(self, db: Session, ip_address: str) -> datetime:
        """Get the time when the rate limit will reset for the given IP."""
        hashed_ip = self._get_hashed_ip(ip_address)

        # Calculate the window start time
        window_start = datetime.utcnow() - timedelta(seconds=self.window_seconds)

        record = db.query(RateLimitRecord).filter(
            RateLimitRecord.ip_address == hashed_ip,
            RateLimitRecord.window_start >= window_start
        ).first()

        if not record:
            # No record exists, return now (meaning no rate limit currently active)
            return datetime.utcnow()

        return record.expires_at
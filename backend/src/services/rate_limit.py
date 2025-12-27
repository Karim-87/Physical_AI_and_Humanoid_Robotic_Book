import time
from typing import Dict
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    """
    Simple in-memory rate limiter to prevent exceeding API quotas.
    """
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)  # API key -> list of request timestamps
        self.limits = {
            'cohere': 5,      # 5 requests per minute per API key
            'qdrant': 100,    # 100 requests per minute per API key
            'gemini': 10,     # 10 requests per minute per API key
        }
        self.time_window = 60  # 1 minute window

    def is_allowed(self, api_key: str, service: str) -> bool:
        """
        Check if a request is allowed based on rate limits.
        """
        current_time = time.time()

        # Remove requests older than the time window
        self.requests[api_key] = [
            req_time for req_time in self.requests[api_key]
            if current_time - req_time < self.time_window
        ]

        # Check if we're under the limit
        current_count = len(self.requests[api_key])
        limit = self.limits.get(service, 10)  # Default to 10 if service not specified

        return current_count < limit

    def record_request(self, api_key: str, service: str):
        """
        Record a request for rate limiting purposes.
        """
        self.requests[api_key].append(time.time())

# Global rate limiter instance
rate_limiter = RateLimiter()
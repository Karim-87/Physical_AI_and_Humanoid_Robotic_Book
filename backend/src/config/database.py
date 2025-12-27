from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from .settings import settings
import logging

logger = logging.getLogger(__name__)

# Create async engine
# Ensure the database URL uses the async driver (asyncpg) instead of psycopg2
# Remove query parameters that are incompatible with asyncpg
db_url = settings.neon_database_url
if '?' in db_url:
    # Split the URL and parameters
    parts = db_url.split('?', 1)
    base_url = parts[0]
    params_str = parts[1] if len(parts) > 1 else ""

    # Parse the parameters and filter out incompatible ones
    params = {}
    for param in params_str.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            # Only keep compatible parameters for asyncpg
            if key not in ['sslmode', 'channel_binding']:
                params[key] = value

    # Reconstruct the URL without incompatible parameters
    if params:
        params_part = '&'.join([f"{k}={v}" for k, v in params.items()])
        db_url = f"{base_url}?{params_part}"
    else:
        db_url = base_url
else:
    base_url = db_url

# Replace the scheme with asyncpg
db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
db_url = db_url.replace("postgres://", "postgresql+asyncpg://")

engine = create_async_engine(
    db_url,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False  # Set to True for debugging SQL queries
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    """Dependency for FastAPI to get database session"""
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Initialize database tables"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import text
    from ..models.chat import Base

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables initialized successfully")
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .settings import settings
import logging

logger = logging.getLogger(__name__)

# --- DATABASE URL FIXING (Neon + asyncpg) ---

db_url = settings.neon_database_url
# Remove incompatible query params
if '?' in db_url:
    base_url, params_str = db_url.split('?', 1)
    params = {}
    for param in params_str.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            if key not in ['sslmode', 'channel_binding']:
                params[key] = value
    if params:
        db_url = base_url + '?' + '&'.join(f"{k}={v}" for k, v in params.items())
    else:
        db_url = base_url

# Ensure async driver
db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")
db_url = db_url.replace("postgres://", "postgresql+asyncpg://")

# --- ASYNC ENGINE (CORRECT) ---

engine = create_async_engine(
    db_url,
    echo=False,   # True only for debugging
)

# --- SESSION FACTORY ---

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --- FASTAPI DEPENDENCY ---

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

# --- INIT DB ---

async def init_db():
    from ..models.chat import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables initialized successfully")


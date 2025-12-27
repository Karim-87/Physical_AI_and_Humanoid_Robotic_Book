from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from datetime import datetime
from src.models.chat import ChatSession, ChatMessage
from src.config.database import AsyncSessionLocal
import uuid

class SessionService:
    def __init__(self):
        pass

    async def get_or_create_session(self, session_id: Optional[str] = None) -> ChatSession:
        """Get existing session or create a new one"""
        async with AsyncSessionLocal() as db:
            if session_id:
                # Try to get existing session
                result = await db.execute(
                    select(ChatSession).where(
                        and_(ChatSession.id == session_id, ChatSession.active == True)
                    )
                )
                session = result.scalar_one_or_none()

                if session:
                    # Update the last access time
                    session.updated_at = datetime.utcnow()
                    await db.commit()
                    return session

            # Create new session
            new_session = ChatSession(
                id=str(uuid.uuid4()),
                active=True
            )
            db.add(new_session)
            await db.commit()
            await db.refresh(new_session)
            return new_session

    async def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        retrieved_chunks: Optional[List[str]] = None,
        mode: Optional[str] = None,
        response_time: Optional[float] = None
    ) -> ChatMessage:
        """Save a message to the session"""
        async with AsyncSessionLocal() as db:
            message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content,
                retrieved_chunks=retrieved_chunks or [],
                mode=mode,
                response_time=response_time
            )
            db.add(message)
            await db.commit()
            await db.refresh(message)
            return message

    async def get_session_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """Get chat history for a session"""
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.timestamp.desc())
                .limit(limit)
            )
            return result.scalars().all()

    async def deactivate_session(self, session_id: str):
        """Deactivate a session"""
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(ChatSession).where(ChatSession.id == session_id)
            )
            session = result.scalar_one_or_none()
            if session:
                session.active = False
                session.updated_at = datetime.utcnow()
                await db.commit()

# Global instance
session_service = SessionService()
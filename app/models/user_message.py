from sqlalchemy import func, Column, Integer, String, DateTime

from app.db.base import Base


class UserMessage(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    message = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

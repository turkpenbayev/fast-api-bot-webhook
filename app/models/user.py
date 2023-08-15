from sqlalchemy import Column, Integer, String

from app.db.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    token = Column(String)

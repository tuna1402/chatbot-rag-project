# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Interval
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

class ChatRoom(Base):
    __tablename__ = 'chatrooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    conversation_duration = Column(Interval)
    user = relationship('User')

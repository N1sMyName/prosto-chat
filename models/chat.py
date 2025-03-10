# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

class Message(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)
    editedAt = Column(DateTime, nullable=True)
    deletedAt = Column(DateTime, nullable=True)
    message = Column(Text, nullable=False)
    senderId = Column(Integer, ForeignKey('user.id'), nullable=False)
    receiverId = Column(Integer, ForeignKey('user.id'), nullable=False)
    isDeleted = Column(Boolean, default=False)
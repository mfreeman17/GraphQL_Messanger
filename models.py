from sqlalchemy import Column, DateTime, Integer, String, VARCHAR, ForeignKey
from sqlalchemy.sql import func

from .database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True, nullable = False)
    author = Column(VARCHAR(20),ForeignKey("users.username"), nullable = False )
    recipient = Column(VARCHAR(20), ForeignKey("users.username"), nullable = False)
    content = Column(VARCHAR(1000), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

class Users(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, index=True, nullable = False)
    username = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(VARCHAR(34), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

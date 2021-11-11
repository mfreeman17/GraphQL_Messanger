from sqlalchemy import Column, DateTime, Integer, VARCHAR, ForeignKey
from sqlalchemy.sql import func

from .database import Base

class Message(Base):
    __tablename__ = "messages"
    ## TODO: change author to authorid and recipient to rec_id
    id = Column(Integer, primary_key=True, index=True, nullable = False)
    author = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False )
    recipient = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
    content = Column(VARCHAR(1000), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

class Users(Base):
    __tablename__= "users"
    id = Column(Integer, primary_key=True, index=True, nullable = False)
    username = Column(VARCHAR(20), unique=True, nullable=False)
    password = Column(VARCHAR(34), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())

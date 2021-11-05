from sqlalchemy import Column, DateTime, Integer, String, VARCHAR
from sqlalchemy.sql import func

from .database import Base
TABLENAME = "post"

class Post(Base):
    __tablename__ = TABLENAME

    id = Column(Integer, primary_key=True, index=True, nullable = False)
    title = Column(VARCHAR(30), nullable = False)
    content = Column(VARCHAR(1000), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


'''


'''

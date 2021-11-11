from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_username= "root"
database_password = "icecream"
database_hostname = "localhost"
database_port = "3306"
database_name = "messaging"

SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector://{database_username}:{database_password}@{database_hostname}:{database_port}/{database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

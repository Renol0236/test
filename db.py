from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Engine = create_engine("postgresql://postgres:123@localhost:5432/testdb")
SessionLocal = sessionmaker(autoflush=True, bind=Engine)
Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)


Base.metadata.create_all(bind=Engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from typing import List

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db, UserDB


class User(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


app = FastAPI()


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users


@app.post("/create_user", response_model=User)
def create_user(user: User, db: Session = Depends(get_db)):
    db_user = UserDB(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

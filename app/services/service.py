from sqlalchemy.orm import Session
from models.user import User
from fastapi import Depends, HTTPException, status
from core.database import get_db


def get_db_user_auth(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user


def get_db_user_registration(email: str, db: Session = Depends(get_db)) -> User | None:
    return db.query(User).filter(User.email == email).first()

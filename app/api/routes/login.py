from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from services.service import get_db_user_auth
from schemas.user import UserIn
from core.database import get_db

router = APIRouter(prefix="/login", tags=["Авторизация"])


@router.get("/", summary="Авторизация пользователя", status_code=status.HTTP_200_OK)
def login_user(user: UserIn, db: Session = Depends(get_db)):
    user = get_db_user_auth(email=user.email, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="")

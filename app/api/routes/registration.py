from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from schemas.user import CreateUser, UserOut
from core.database import get_db
from models.user import User
from services.service import get_db_user_registration
import bcrypt

router = APIRouter(prefix="/registration", tags=["Регистрация"])


@router.post(
    "/labrarian/",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
)
def registration_user(user: CreateUser, db: Session = Depends(get_db)) -> UserOut:
    existing_user = get_db_user_registration(email=user.email, db=db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким Email зарегистрирован!",
        )
    password_bytes = user.password.encode("utf-8")  # Конвектируем строку в bytes
    salt = bcrypt.gensalt()  # Случайная и уникальная строка символов
    hashed_password = bcrypt.hashpw(
        password=password_bytes, salt=salt
    )  # Хэширование пароля
    db_librarian = User(email=user.email, hashed_password=hashed_password)
    db.add(db_librarian)
    db.commit()
    db.refresh(db_librarian)
    return UserOut(email=user.email)

from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from schemas.user import CreateUser, UserOut
from core.database import get_db
from schemas.librarian import CreateLibrarian, LibrarianOut
from models.librarian import Librarian
from models.user import User
import bcrypt

router = APIRouter(prefix="/registration", tags=["Регистрация"])


def get_db_user(email: str, db: Session = Depends(get_db)) -> bool:
    """
    Проверяет зарегистрирован ли email такой в базе данных.

    Args:
        email (str): Email пользователя
        db (Session, optional): Сессия баз данных.

    Returns:
        bool: Возвращает булевое значение.
    """
    return db.query(User).filter(User.email == email).first() is not None


@router.post(
    "/user/",
    summary="Регистрация пользователей",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOut,
)
def registration_user(new_user: CreateUser, db: Session = Depends(get_db)) -> UserOut:
    """
    Регистрация нового пользователя.

    Args:
        new_user (CreateUser): Данные для регистрации нового пользователя, включая:
            - username (str): Имя пользователя.
            - email (EmailStr): Электронная почта.
        db (Session): Сессия баз данных.

    Raises:
        HTTPException: _description_

    Returns:
        UserOut:
    """
    existing_user = get_db_user(email=new_user.email, db=db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован",
        )
    db_user = User(username=new_user.username, email=new_user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post(
    "/labrarian/",
    summary="Регистрация библиотекорей",
    status_code=status.HTTP_201_CREATED,
    response_model=LibrarianOut,
)
def registration_librarian(
    librarian: CreateLibrarian, db: Session = Depends(get_db)
) -> LibrarianOut:
    password_bytes = librarian.password.encode("utf-8")  # Конвектируем строку в bytes
    salt = bcrypt.gensalt()  # Случайная и уникальная строка символов
    hashed_password = bcrypt.hashpw(
        password=password_bytes, salt=salt
    )  # Хэширование пароля
    db_librarian = Librarian(email=librarian.email, hashed_password=hashed_password)
    db.add(db_librarian)
    db.commit()
    db.refresh(db_librarian)
    return LibrarianOut(email=librarian.email)

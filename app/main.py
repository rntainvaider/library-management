from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db, init_db
from schemas.librarian import CreateLibrarian, LibrarianOut
from schemas.user import CreateUser, UserOut
from models.librarian import Librarian
from models.user import User

import bcrypt

app = FastAPI()

init_db()  # Создание таблиц


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


@app.get("/")
def hello():
    return "Hello world"


@app.post(
    "/register/labrarian",
    tags=["Регистрация"],
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


# @app.post(
#     "/registretion/user/",
#     tags=["Регистрация"],
#     summary="Регистрация пользователей",
#     status_code=status.HTTP_201_CREATED,
#     response_model=UserOut,
# )
# def registration_user(new_user: CreateUser, db: Session = Depends(get_db)) -> UserOut:
#     """
#     Регистрация нового пользователя.

#     Args:
#         new_user (CreateUser): Данные для регистрации нового пользователя, включая:
#             - username (str): Имя пользователя.
#             - email (EmailStr): Электронная почта.
#         db (Session): Сессия баз данных.

#     Raises:
#         HTTPException: _description_

#     Returns:
#         UserOut:
#     """
#     existing_user = get_db_user(email=new_user.email, db=db)
#     if existing_user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Email уже зарегистрирован",
#         )
#     db_user = User(username=new_user.username, email=new_user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

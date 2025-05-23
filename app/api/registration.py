from fastapi import status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..main import get_db_user
from schemas.user import CreateUser, UserOut
from ..core.database import get_db
from ..models.user import User


@routes.post(
    "/registretion/user/",
    tags=["Регистрация"],
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

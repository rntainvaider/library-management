from sqlalchemy import Column, String, Integer, LargeBinary
from .base import Base


class User(Base):
    """Модель библиотекаря"""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(
        LargeBinary, nullable=False
    )  # Для хранения бинарных данных

    def __repr__(self) -> str:
        return f"<Librarian(id={self.id}, email={self.email})>"

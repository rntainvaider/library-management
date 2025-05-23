from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL
from models.base import Base

# Создание движка БД
engine = create_engine(DATABASE_URL)

# Создани фабрики сессий
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    """Генератор сессий для зависимостей"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Инициализация БД (Создание таблиц)
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

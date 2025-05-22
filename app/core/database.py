from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from config import DATABASE_URL

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

# Инициализация БД (Создани таблиц)ё
def init_db() -> None:
    Base.metadata.create_all(bind=engine)

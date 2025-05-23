from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session
from core.database import get_db, init_db
from schemas.librarian import CreateLibrarian, LibrarianOut
from models.librarian import Librarian
from models.user import User
from api.routes.registration import router

app = FastAPI()

# Подключение маршрутов
app.include_router(router)

init_db()  # Создание таблиц


@app.get("/")
def hello():
    return "Hello world"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

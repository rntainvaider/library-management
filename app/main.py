from fastapi import FastAPI
from core.database import init_db
from api.routes.registration import router as registration
from api.routes.login import router as login

app = FastAPI()

# Подключение маршрутов
app.include_router(registration)
app.include_router(login)

init_db()  # Создание таблиц


@app.get("/")
def hello():
    return "Hello world"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

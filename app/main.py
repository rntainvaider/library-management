from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return "Hello world"

@app.post("/register/", tags=["Регистрация"], summary="Регистрация пользователей")
def registration():
    return "Registration"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

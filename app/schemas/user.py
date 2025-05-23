from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    password: str
    email: EmailStr


class UserIn(CreateUser):
    pass


class UserOut(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True  # Автоматически преобразует ORM-модель в свою модель

from pydantic import BaseModel, EmailStr


class CreateLibrarian(BaseModel):
    password: str
    email: EmailStr


class LibrarianOut(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True  # Автоматически преобразует ORM-модель в свою модель

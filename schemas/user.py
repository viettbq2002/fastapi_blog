from pydantic import BaseModel, EmailStr, Field

from db.models.user import Role


class UserCreate(BaseModel):
    email: EmailStr
    # ... mean this field is required or a placeholder
    password: str = Field(..., min_length=8)


class UserLogin(UserCreate):
    pass


class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class ShowAllUser(ShowUser):
    role: Role

    class Config:
        orm_mode = True

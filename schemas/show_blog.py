from datetime import date
from typing import Optional
from pydantic import BaseModel


class BlogCategory(BaseModel):
    id: int
    name: str
    description: str | None

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    id: int
    title: str
    slug: str
    content: Optional[str]
    created_at: date
    categories: list[BlogCategory]

    class Config:
        orm_mode = True

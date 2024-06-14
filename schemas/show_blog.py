from datetime import date
from typing import Optional
from pydantic import BaseModel


class ShowBlog(BaseModel):
    id: int
    title: str
    slug: str
    content: Optional[str]
    created_at: date

    class Config:
        orm_mode = True

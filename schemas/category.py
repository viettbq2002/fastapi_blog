from pydantic import BaseModel
from typing import Optional

from schemas.show_blog import ShowBlog
from schemas.show_category import ShowCategory


class CreateCategory(BaseModel):
    name: str
    description: Optional[str] = None


class ShowCategoryDetail(ShowCategory):
    blogs: list[ShowBlog]

    class Config:
        orm_mode = True

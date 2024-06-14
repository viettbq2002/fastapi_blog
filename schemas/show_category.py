from typing import Optional
from pydantic import BaseModel


class ShowCategory(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        orm_mode = True

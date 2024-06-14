from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from enum import Enum


class Role(Enum):
    ADMIN = "admin"
    AUTHOR = "author"


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(SQLAlchemyEnum(Role), default=Role.AUTHOR)
    is_active = Column(Boolean(), default=True)
    blogs = relationship("Blog", back_populates="author")

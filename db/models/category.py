from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base_class import Base
from db.models.blog_category import blog_category


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    blogs = relationship("Blog", secondary=blog_category, back_populates="categories")

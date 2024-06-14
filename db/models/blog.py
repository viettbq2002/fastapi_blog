from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db.base_class import Base
from db.models.blog_category import blog_category
from db.models.category import Category


class Blog(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    content = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="blogs")
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=False)
    categories = relationship(
        "Category", secondary=blog_category, back_populates="blogs"
    )

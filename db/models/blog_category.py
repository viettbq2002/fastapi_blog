from sqlalchemy import Column, Integer, String, ForeignKey, Table
from db.base_class import Base


blog_category = Table(
    "blog_category",
    Base.metadata,
    Column("blog_id", Integer, ForeignKey("blog.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)

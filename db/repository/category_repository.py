from db.repository.blog_repository import get_blog_by_id
from schemas.category import CreateCategory
from sqlalchemy.orm import Session
from db.models.category import Category


def create_category(payload: CreateCategory, db: Session):
    category = Category(**payload.dict())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_category_by_id(id: int, db: Session) -> Category | None:
    return db.query(Category).filter(Category.id == id).first()


def get_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def add_blog(category_id: int, blog_id: int, db: Session):
    category = get_category_by_id(category_id, db)
    blog = get_blog_by_id(blog_id, db)
    if not category:
        return
    category.blogs.append(blog)
    db.add(category)
    db.commit()
    db.refresh(category)


    
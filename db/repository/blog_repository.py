from schemas.blog import CreateBlog, UpdateBlog
from sqlalchemy.orm import Session
from db.models.blog import Blog


def create_new_blog(payload: CreateBlog, db: Session, author_id: int):
    blog = Blog(
        **payload.dict(), author_id=author_id
    )  # **payload.dict() = payload.title, payload.content
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def get_blog_by_id(id: int, db: Session) -> Blog | None:
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog


def list_blog(db: Session) -> list[Blog]:

    blogs = db.query(Blog).filter(Blog.is_active == True).all()
    return blogs


def update_blog(id: int, blog: UpdateBlog, author_id: int, db: Session):
    blog_in_db = get_blog_by_id(id, db)
    if not blog_in_db:
        return
    if blog_in_db.author_id != author_id:
        return
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    blog_in_db.slug = blog.title.replace(" ", "-").lower()
    db.add(blog_in_db)
    db.commit()
    return blog_in_db


def active_blog(id: int, db: Session):
    blog_in_db = get_blog_by_id(id, db)
    if not blog_in_db:
        return
    blog_in_db.is_active = True
    db.add(blog_in_db)
    db.commit()
    return blog_in_db


def delete_blog(id: int, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error": "Blog not found"}
    if blog_in_db.first().author_id != author_id:
        return {"error": "Only the author can delete the blog"}
    blog_in_db.delete()

    db.commit()
    return {"message": "Blog deleted"}



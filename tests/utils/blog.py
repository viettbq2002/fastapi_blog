from sqlalchemy.orm import Session
from db.repository.blog_repository import create_new_blog
from schemas.blog import CreateBlog
from tests.utils.user import create_random_user


def create_random_blog(db: Session):
    blog = CreateBlog(
        title="Hello World",
        content="Hello World This is my first blog test",
        slug="hello-world",
    )
    user = create_random_user(db)
    blog = create_new_blog(author_id=user.id, payload=blog, db=db)
    return blog

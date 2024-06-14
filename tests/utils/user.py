from sqlalchemy.orm import Session
from db.repository.user_repository import create_new_user
from schemas.user import UserCreate


def create_random_user(db: Session):
    user = UserCreate(
        email="quocviet@gmail.com",
        password="HelloWorldFucked",
    )
    return create_new_user(db=db, payload=user)

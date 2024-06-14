from sqlalchemy.orm import Session

from schemas.user import UserCreate
from db.models.user import User, Role
from core.hashing import Hasher


def create_new_user(payload: UserCreate, db: Session):
    user = User(
        email=payload.email, password=Hasher.get_password_hash(payload.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter(User.email == email).first()
    return user


def assign_admin(id: int, db: Session):
    user = get_user_by_id(id, db)
    if not user:
        return
    user.role = Role.ADMIN
    db.add(user)
    db.commit()
    return user

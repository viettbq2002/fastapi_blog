from core.hashing import Hasher
from db.models.auth import JwtToken
from db.repository.user_repository import create_new_user, get_user_by_email
from db.session import get_db
from fastapi import APIRouter, Depends, Response, status, HTTPException

from sqlalchemy.orm import Session
from core.sercurity import create_access_token
from schemas.token import Token
from schemas.user import ShowUser, UserCreate, UserLogin
from fastapi.exceptions import HTTPException


router = APIRouter()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email, db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


@router.post("/login", response_model=Token)
def login_for_access_token(
    response: Response,
    payload: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(payload.email, payload.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt_payload = JwtToken(role=user.role.value, sub=user.email).dict()
    access_token = create_access_token(data=jwt_payload)
    response.set_cookie("token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
       Args:
           user (UserCreate): The user data to create.
           db (Session, optional): The database session. Defaults to Depends(get_db).

       Returns:
           ShowUser
    """
    user = create_new_user(user, db)
    return user


@router.delete("/logout")
def logout(response: Response):
    response.delete_cookie(httponly=True, key="token")
    return {"message": "logout success"}

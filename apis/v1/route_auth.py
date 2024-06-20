from core.hashing import Hasher
from db.models.user import Role, User
from db.repository.user_repository import create_new_user, get_user_by_email
from db.session import get_db
from fastapi import APIRouter, Depends, Response, status, HTTPException
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session
from core.sercurity import create_access_token
from core.config import settings
from schemas.token import Token
from schemas.user import ShowUser, UserCreate, UserLogin
from jose import JWTError, jwt
from fastapi.exceptions import HTTPException

from services.user_service import get_user_from_cookie

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
    access_token = create_access_token(data={"sub": user.email})
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
    response.delete_cookie("token")
    return {"message": "logout success"}


auth_scheme = HTTPBearer()


def get_current_user(
    headers: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(get_db),
):
    token = headers.credentials
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=email, db=db)
    if user is None:
        raise credentials_exception
    return user


def check_admin(current_user=Depends(get_current_user)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not has perrmission to perform requested action",
        )


def check_admin_cookie(current_user: User = Depends(get_user_from_cookie)):
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not has permission to perform requested action",
        )

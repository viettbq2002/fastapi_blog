from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from apis.v1.route_auth import check_admin, check_admin_cookie, get_current_user
from db.models.user import User
from schemas.user import ShowAllUser, ShowUser
from db.session import get_db
from db.repository.user_repository import assign_admin, get_user_by_id, get_users
from services.user_service import get_user_from_cookie

router = APIRouter()


@router.patch("/assign_admin/{id}", dependencies=[Depends(check_admin)])
async def assign_user_to_admin(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Assigns a user to an admin based on the given ID.

    Access by admin only.

    Parameters:

        id (int): The ID of the user to assign.

        db (Session): The database session.

    Returns:

        dict: A message indicating the user has been assigned to an admin.
    """
    user = assign_admin(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return {"message": "User assigned to admin"}


@router.get(
    "", response_model=list[ShowAllUser], dependencies=[Depends(check_admin_cookie)]
)
async def get_all_users(db: Session = Depends(get_db)):
    users = get_users(db)
    return users


@router.get("/cookie/me", response_model=ShowAllUser)
def cookie_auth(user: User = Depends(get_user_from_cookie)):
    return user


@router.get("/me", response_model=ShowAllUser)
async def get_login_user(current_user: User = Depends(get_current_user)):
    """
    Retrieves a current login user

    Parameters:
        id (int): The ID of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ShowUser
    """
    return current_user


@router.get(
    "/{id}",
    response_model=ShowUser,
    responses={status.HTTP_404_NOT_FOUND: {"description": "User not found"}},
)
async def get_user(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a user by their ID.

    Parameters:
        id (int): The ID of the user.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ShowUser
    """
    user = get_user_by_id(id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user

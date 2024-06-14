from apis.v1.route_auth import check_admin
from db.repository.category_repository import (
    create_category,
    get_category_by_id,
    get_categories,
    add_blog,
)
from schemas.category import CreateCategory, ShowCategoryDetail
from db.session import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter, status

from schemas.show_category import ShowCategory


router = APIRouter()


@router.post(
    "",
    response_model=ShowCategory,
    dependencies=[Depends(check_admin)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Not authenticated"},
        status.HTTP_403_FORBIDDEN: {"description": "Not has permission"},
    },
)
async def create_a_category(payload: CreateCategory, db: Session = Depends(get_db)):
    """
    Create a new category based on the provided payload.

    Parameters:
    - payload: CreateCategory object containing information about the new category.
    - db: Session object for the database connection.

    Returns:
    - ShowCategory: The newly created category as a ShowCategory object.
    """
    created_category = create_category(payload, db)
    return created_category


@router.get("", response_model=list[ShowCategory])
async def get_all_category(db: Session = Depends(get_db)):
    """
    Get all categories from the database.

    Parameters:

    - db (Session): The database session. Defaults to the session obtained from the `get_db` dependency.

    Returns:

    - list[ShowCategory]: A list of `ShowCategory` objects representing all categories in the database.
    """
    categories = get_categories(db)
    return categories


@router.get("/{id}", response_model=ShowCategoryDetail)
async def get_category_detail(id: int, db: Session = Depends(get_db)):
    category = get_category_by_id(id, db)
  
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/add-blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def add_blog_to_category(id: int, blog_id: int, db: Session = Depends(get_db)):
    add_blog(id, blog_id, db)

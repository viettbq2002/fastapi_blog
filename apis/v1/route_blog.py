from fastapi import Depends, APIRouter, HTTPException, status
from apis.v1.route_auth import get_current_user
from db.models.user import User
from db.repository.blog_repository import (
    active_blog,
    create_new_blog,
    delete_blog,
    get_blog_by_id,
    list_blog,
    update_blog,
)
from db.session import get_db
from sqlalchemy.orm import Session
from schemas.blog import CreateBlog, UpdateBlog
from schemas.show_blog import ShowBlog

router = APIRouter()


@router.post("", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: CreateBlog,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new blog.

    This function creates a new blog based on the provided `blog` object. It requires a valid `CreateBlog` object and a database session (`db`). The current user is also required, but it is obtained using the `get_current_user` dependency.

    Parameters:

        - blog (CreateBlog): The blog object containing the data for the new blog.

        - db (Session, optional): The database session. Defaults to the result of the `get_db` dependency.

        - current_user (User, optional): The current user. Defaults to the result of the `get_current_user` dependency.
    Returns:

        - ShowBlog: The newly created blog object.

    Raises:

        - 401 (HTTP_401_UNAUTHORIZED): If the current user is not authenticated.

    Status Code:

        - 201 (HTTP_201_CREATED): The blog was successfully created.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    blog = create_new_blog(blog, db, author_id=current_user.id)
    return blog


@router.get(
    "/{id}",
    response_model=ShowBlog,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Blog not found"}},
)
async def get_blog(
    id: int,
    db: Session = Depends(get_db),
):
    """
    Get a blog by its ID.

    Parameters:
        - id (int): The ID of the blog to retrieve.
        - db (Session, optional): The database session to use. Defaults to the session obtained from the `get_db` dependency.

    Returns:
        - ShowBlog: The retrieved blog.

    Raises:
        - HTTPException: If the blog with the given ID is not found.

    Responses:
        - 200 (ShowBlog): The retrieved blog.
        - 404 (HTTPException): If the blog with the given ID is not found.
    """
    blog = get_blog_by_id(id, db)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    return blog


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[ShowBlog],
)
async def get_all_blog(db: Session = Depends(get_db)):
    """
    Get all blogs from the database.

    Parameters:
        - db (Session, optional): The database session to use. Defaults to the session obtained from the `get_db` dependency.

    Returns:
        - list[ShowBlog]: A list of all the blogs in the database.

    Raises:
        - None

    Status Code:
        - 200 (OK): The request was successful and the response contains the list of blogs.
    """
    blog = list_blog(db)
    return blog


@router.put(
    "/{id}",
    response_model=ShowBlog,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Blog not found"}},
)
async def update_a_blog(
    id: int,
    blog: UpdateBlog,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Updates a blog with the given ID.

    Parameters:
        - id (int): The ID of the blog to be updated.

        - blog (UpdateBlog): The updated blog object.

        - db (Session, optional): The database session. Defaults to the result of the `get_db` dependency.

    Returns:

        - ShowBlog: The updated blog object.

    Raises:

        - HTTPException: If the blog with the given ID is not found.

    """
    blog = update_blog(id, blog, author_id=current_user.id, db=db)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    return blog


@router.patch(
    "/{id}/active",
    response_model=ShowBlog,
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Blog not found"}},
)
async def active_a_blog(id: int, db: Session = Depends(get_db)):
    """
    Activate a blog with the given ID.

    Parameters:
        - id (int): The ID of the blog to be activated.

        - db (Session, optional): The database session. Defaults to the result of the `get_db` dependency.

    Returns:

        - ShowBlog: The activated blog object with an additional "message" field indicating success.

    Raises:

        - HTTPException: If the blog with the given ID is not found.
    """
    blog = active_blog(id, db)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )

    return blog


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Blog not found"}},
)
async def delete_a_blog(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = delete_blog(id, current_user.id, db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_404_NOT_FOUND
        )

    return message

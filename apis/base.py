from fastapi import APIRouter
from apis.v1 import route_user, route_blog, route_auth, route_category

api_router = APIRouter()
api_router.include_router(route_user.router, prefix="/users", tags=["users"])
api_router.include_router(route_blog.router, prefix="/blogs", tags=["blogs"])
api_router.include_router(route_auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(route_category.router, prefix="/categories", tags=["category"])

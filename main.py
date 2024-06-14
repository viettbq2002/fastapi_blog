from fastapi import FastAPI
from core.config import settings
from apis.base import api_router

from fastapi.middleware.cors import CORSMiddleware


def include_router(app: FastAPI):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    return app


app = start_application()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
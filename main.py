from fastapi import FastAPI
from core.config import settings
from apis.base import api_router

from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    print(settings.DATABASE_URL)
    return {"message": "Your API Worked"}

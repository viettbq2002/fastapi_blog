from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from jose import ExpiredSignatureError
from core.config import settings
from apis.base import api_router

from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:3000"]


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.exception_handler(ExpiredSignatureError)
async def handle_exception(request, exc):
    response = JSONResponse(
        content={"detail": "Token Expired"},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    response.delete_cookie("token")
    return response


@app.get("/")
def root():
    print(settings.DATABASE_URL)
    return {"message": "Your API Worked"}

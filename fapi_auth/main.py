from fastapi import APIRouter, FastAPI

from .db import Base, engine
from .routers.auth import auth_router
from .routers.users import user_router

api_router = APIRouter(prefix="/api/v1")


Base.metadata.create_all(bind=engine)

api_router.include_router(auth_router)
api_router.include_router(user_router)

app = FastAPI()
app.include_router(api_router)

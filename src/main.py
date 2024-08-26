import uvicorn
from fastapi import FastAPI

from fastapi_users import FastAPIUsers

from .base import fastapi_users

from src.auth.manager import get_user_manager
from src.auth.models import User

from .auth.base import auth_backend
from .auth.schemas import UserCreate, UserRead, UserUpdate
from .notes.router import router as notes_router

app = FastAPI(title="Notes")

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

# app.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )

# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate),
#     prefix="/users",
#     tags=["users"],
# )

app.include_router(notes_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8080,
        log_level="info",
        reload=True
    )
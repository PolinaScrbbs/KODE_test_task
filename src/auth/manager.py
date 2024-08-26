from typing import Any, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, exceptions
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .shemas import UserCreate
from .models import User
from ..database import get_async_session
from ..config import settings

class UserManager(BaseUserManager[User, int]):
    reset_password_token_secret = settings.SECRET_AUTH
    verification_token_secret = settings.SECRET_AUTH

    def __init__(self, session: AsyncSession, user_db):
        self.session = session
        self.user_db = user_db
        self.password_helper = PasswordHelper()

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.email} has registered.")

    def parse_id(self, user_id: Any) -> int:
        return int(user_id)

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_create: UserCreate, safe: bool = False, request: Optional[Request] = None) -> User:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.get_by_email(user_create.email)
        if existing_user:
            raise exceptions.UserAlreadyExists()

        user_dict = user_create.dict(exclude_unset=True)
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)

        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)
        return created_user


async def get_user_manager(session: AsyncSession = Depends(get_async_session)):
    user_db = SQLAlchemyUserDatabase(session, User)
    yield UserManager(session, user_db)
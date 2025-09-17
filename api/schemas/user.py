from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from api.models.user import User
from api.utils.password import get_password_hash

class BaseUser(BaseModel):
    email: EmailStr
    username: Annotated[str, Field(min_length=5, max_length=30)]


class UserCreate(BaseUser):
    password: Annotated[str, Field(min_length=8, max_length=64)]

    def to_model(self) -> User:
        return User(
            email=self.email,
            username=self.username,
            hashed_password=get_password_hash(self.password),
        )

class UserResponse(BaseUser):
    pass

import strawberry
from sqlalchemy.orm import Session
from app.database import get_db
from app.ms_auth import crud
from app.ms_auth.types import UserType
import hashlib


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def create_user(self, username: str, email: str, password: str) -> UserType:
        db: Session = next(get_db())
        user_data = {
            "username": username,
            "email": email,
            "hashed_password": hash_password(password)
        }
        user = crud.create_user(db, user_data)
        return UserType(id=user.id, username=user.username, email=user.email)


@strawberry.type
class UserQuery:
    @strawberry.field
    def get_user_by_email(self, email: str) -> UserType:
        db: Session = next(get_db())
        user = crud.get_user(db, email)
        if not user:
            raise Exception("User not found")
        return UserType(id=user.id, username=user.username, email=user.email)

    @strawberry.field
    def get_all_users(self) -> list[UserType]:
        db: Session = next(get_db())
        return [UserType(id=c.id, username=c.username, email=c.email) for c in crud.get_users(db)]

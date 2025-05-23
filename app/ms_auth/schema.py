import strawberry
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.ms_auth import crud
from app.ms_auth.types import UserType
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
alg = os.getenv('ALGORITHM')


@strawberry.type
class TokenType:
    access_token: str


@strawberry.type
class UserMutation:
    @strawberry.mutation()
    def create_user(self, username: str, email: str, password: str) -> UserType:
        db: Session = next(get_db())
        user_data = {
            "username": username,
            "email": email,
            "hashed_password": crud.hash_password(password)
        }
        user = crud.create_user(db, user_data)
        return UserType(id=user.id, username=user.username, email=user.email)

    @strawberry.mutation()
    def login(self, user_email: str, password: str) -> TokenType:
        db: Session = next(get_db())
        user = crud.get_user(db, user_email)

        if not user or not crud.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Неверный логин или пароль")

        token_data = {"sub": user.username}
        token = jwt.encode(token_data, secret_key, algorithm=alg)
        return TokenType(access_token=token)


@strawberry.type
class UserQuery:
    @strawberry.field()
    def get_user_by_email(self, email: str) -> UserType:
        db: Session = next(get_db())
        user = crud.get_user(db, email)
        if not user:
            raise Exception("User not found")
        return UserType(id=user.id, username=user.username, email=user.email)

    @strawberry.field()
    def get_all_users(self) -> list[UserType]:
        db: Session = next(get_db())
        return [UserType(id=c.id, username=c.username, email=c.email) for c in crud.get_users(db)]

from sqlalchemy.orm import Session
from app.ms_auth.models import User
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'])


def get_user(db: Session, user_email: str):
    return db.query(User).filter(User.email == user_email).first()


def get_users(db: Session,  skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user_data: dict) -> User:
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

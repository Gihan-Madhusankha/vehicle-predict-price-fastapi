from passlib.context import CryptContext
from sqlalchemy.orm import Session

import database
from models import User, users
from response import create_response
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to hash a password
def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_user(
        db: Session,
        username: str,
        email: str,
        password: str,
):
    hashed_password = get_password_hash(password)

    print('username > ', username)
    print('email > ', email)
    print('hashed_password  > ', hashed_password)

    db_user = User(username=username, email=email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return create_response("success", "User created successfully", data={"user_id": db_user.id})


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def login_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and verify_password(password, user.password):
        return user
    else:
        return None


from app.db.models import Users
from sqlalchemy.orm import Session

import app.api.users.users_schema as schemas


def create_user(db: Session, user_create: schemas.UserCreateRequest):
    db_user = Users(
        cuid=user_create.cuid,
        user_name=user_create.user_name,
        email=user_create.email,
        password=user_create.password,
        create_date=user_create.create_date,
        discription=user_create.discription,
    )
    db.add(db_user)
    db.commit()
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(Users).filter(Users.email == email).first()


def get_user_by_user_name(db: Session, user_name: str):
    return db.query(Users).filter(Users.user_name == user_name).all()

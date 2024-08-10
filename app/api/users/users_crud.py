from app.db.models import Users
from sqlalchemy.orm import Session
from bcrypt import hashpw, gensalt, checkpw
import app.api.users.users_schema as schemas


def create_user(db: Session, user_create: schemas.UserCreateRequest) -> Users:
    db_user = Users(
        cuid=user_create.cuid,
        user_name=user_create.user_name,
        email=user_create.email,
        password=user_create.password,
        create_date=user_create.create_date,
        description=user_create.description,
    )
    db.add(db_user)
    db.commit()
    return db_user


def update_user(db: Session, user_update: schemas.UserUpdateRequest) -> Users:
    res_user = get_user_by_cuid(db, user_update.cuid)

    # 사용자 정보 업데이트
    for key, value in user_update.dict().items():
        if value is None:
            continue
        if key == 'password':
            value = hashpw(value.encode('utf-8'), gensalt()).decode('utf-8')

        setattr(res_user, key, value)

    db.commit()
    #db.refresh(res_user)

    return res_user


def get_user_by_email(db: Session, email: str, read_all: bool = False) -> Users:
    if read_all:
        return db.query(Users).filter(Users.email == email).all()
    else:
        return db.query(Users).filter(Users.email == email).first()


def get_user_by_user_name(db: Session, user_name: str, read_all: bool = False) -> Users:
    if read_all:
        return db.query(Users).filter(Users.user_name == user_name).all()
    else:
        return db.query(Users).filter(Users.user_name == user_name).first()


def get_user_by_cuid(db: Session, cuid: str, read_all: bool = False) -> Users:
    if read_all:
        return db.query(Users).filter(Users.cuid == cuid).all()
    else:
        return db.query(Users).filter(Users.cuid == cuid).first()

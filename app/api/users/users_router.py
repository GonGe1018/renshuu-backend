from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from bcrypt import checkpw
from typing import Annotated

from datetime import datetime, timedelta
from jose import jwt

import app.api.users.users_schema as schemas
import app.api.users.users_crud as crud
import app.api.users.user_auth as auth
from app.db.database import get_db
import app.core.config as config

router = APIRouter()


@router.post("/create_user")
def create_user(item: schemas.UserCreateRequest,
                db: Session = Depends(get_db)):
    print(item)

    # 약관 동의 여부
    if item.is_confirmed is False:
        raise HTTPException(status_code=400, detail="User has not confirmed")

    # DB와 중복 검사
    if crud.get_user_by_email(db, item.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # DB에 저장
    crud.create_user(db, item)

    data = schemas.UserCreateResponse(
        cuid=item.cuid,
        user_name=item.user_name,
        email=item.email,
        create_date=item.create_date,
        is_confirmed=item.is_confirmed
    )

    return data


@router.post("/login_user")
def login_user(item: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = item.username
    password = item.password

    user_res = crud.get_user_by_email(db, email, read_all=False)

    if user_res is None:
        raise HTTPException(status_code=400, detail="Incorrect account information")

    print(password, user_res.password)
    if checkpw(password.encode('utf-8'), user_res.password.encode('utf-8')):
        access_token = auth.encode_access_token(user_res.cuid)

        data = schemas.UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            cuid=user_res.cuid,
            email=email
        )
        return data

    raise HTTPException(status_code=400, detail="Incorrect account information")


@router.get("/read_user/{user_name}")
def read_user(user_name: str, db: Session = Depends(get_db)):
    user_res = crud.get_user_by_user_name(db, user_name, read_all=True)

    res = []
    for i in user_res:
        user_info = {
            "user_name": i.user_name,
            "description": i.description
        }
        res.append(user_info)

    return res


@router.put("/update_user")
def update_user(item: schemas.UserUpdateRequest,
                db: Session = Depends(get_db),
                current_user: schemas.UserCreateRequest = Depends(auth.get_current_user)):
    # 현재 인증된 사용자가 업데이트 요청을 보낸 사용자와 일치하는지 확인
    if current_user.cuid != item.cuid:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    res_user = crud.update_user(db, item)

    data = schemas.UserUpdateRseponse(
        cuid=res_user.cuid,
        user_name=res_user.user_name,
        email=res_user.email,
        description=res_user.description
    )

    return current_user


@router.delete("/delete_user")
def delete_user(item: schemas.UserDeleteRequest):
    pass

# create, read, update, delete

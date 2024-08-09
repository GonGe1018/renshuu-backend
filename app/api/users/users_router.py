from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

import app.api.users.users_schema as schemas
import app.api.users.users_crud as crud
from app.db.database import get_db

router = APIRouter()


@router.post("/create_user")
def create_user(item: schemas.UserCreateRequest, db: Session = Depends(get_db)):
    print(item)

    # 약관 동의 여부
    if item.is_confirmed is False:
        raise HTTPException(status_code=400, detail="User has not confirmed")

    # DB와 중복 검사
    if crud.get_user_by_email(db, item.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # DB에 저장
    crud.create_user(db, item)

    response = schemas.UserCreateResponse(
        cuid=item.cuid,
        user_name=item.user_name,
        email=item.email,
        create_date=item.create_date,
        is_confirmed=item.is_confirmed
    )

    return {"res": "SUCCESS", "info": response}


@router.get("/read_user/{user_name}")
def read_user(user_name: str, db: Session = Depends(get_db)):
    user_res = crud.get_user_by_user_name(db, user_name)

    res = []
    for i in user_res:
        user_info = {
            "user_name": i.user_name,
            "discription": i.discription
        }
        res.append(user_info)

    return res


@router.put("/update_user")
def update_user(item: schemas.UserUpdateRequest):
    pass


@router.delete("/delete_user")
def delete_user(item: schemas.UserDeleteRequest):
    pass

# create, read, update, delete

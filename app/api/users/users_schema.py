from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, field_validator
import cuid
from bcrypt import hashpw, gensalt, checkpw
from typing import Optional


class UserCreateRequest(BaseModel):
    cuid: str = Field(default_factory=cuid.cuid)
    user_name: str
    email: EmailStr
    password: str
    discription: Optional[str] = Field(default=None)
    is_confirmed: bool = Field(default=False)
    create_date: datetime = Field(default_factory=datetime.now)

    @field_validator('password', mode='before')
    def hash_password(cls, value: str) -> str:
        pw = hashpw(value.encode('utf-8'), gensalt())
        return pw.decode('utf-8')


class UserCreateResponse(BaseModel):
    cuid: str
    user_name: str
    email: EmailStr
    is_confirmed: bool
    create_date: datetime


class UserReadRequest(BaseModel):
    user_name: str
    email: EmailStr
    is_active: bool


class UserLoginRequest(BaseModel):
    user_name: str
    password: str


class UserDeleteRequest(BaseModel):
    cuid: str
    user_name: str
    password: str
    is_confirmed: bool


class UserUpdateRequest(BaseModel):
    cuid: str
    user_name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]

# # 사용 예시
# new_user = UserCreate(user_name="testuser", email="e@x.com", password="mypassword", is_confirmed=True)
# print(new_user.cuid)

# print(new_user.password)  # 출력된 비밀번호는 해시된 상태입니다.
# print(checkpw("mypasswordd".encode('utf-8'), new_user.password.encode('utf-8')))

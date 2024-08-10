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
    description: Optional[str] = Field(default=None)
    is_confirmed: bool = Field(default=False)
    create_date: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_name": "a",
                    "email": "a@a.com",
                    "password": "a",
                    "description": "A very nice Item",
                    "is_confirmed": True
                }
            ]
        }
    }

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
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    cuid: str
    access_token: str
    token_type: str
    email: EmailStr


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
    description: Optional[str]


class UserUpdateRseponse(BaseModel):
    cuid: str
    user_name: str
    email: str
    description: str

# # 사용 예시
# new_user = UserCreate(user_name="testuser", email="e@x.com", password="mypassword", is_confirmed=True)
# print(new_user.cuid)

# print(new_user.password)  # 출력된 비밀번호는 해시된 상태입니다.
# print(checkpw("mypasswordd".encode('utf-8'), new_user.password.encode('utf-8')))

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

import app.core.config as config
import app.api.users.users_crud as crud
from app.db.database import get_db
from app.db.models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login_user")


def encode_access_token(cuid: str,
                        minutes: int = config.settings.access_token_expire_minutes) -> str:
    jwt_data = {
        "sub": cuid,
        "exp": datetime.utcnow() + timedelta(minutes=minutes)
    }

    access_token = jwt.encode(jwt_data, config.settings.secret_key, algorithm=config.settings.algorithm)

    return access_token


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)) -> Users:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print(token)

    # 토큰 디코딩
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=config.settings.algorithm)
        cuid = payload.get("sub")
        exp = payload.get("exp")

        # 토큰의 만료 여부 확인
        if exp is None or datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(tz=timezone.utc):
            print(1)
            raise credentials_exception

        if cuid is None:
            print(2)
            raise credentials_exception

    except JWTError as e:
        print(e)
        raise credentials_exception

    user_res = crud.get_user_by_cuid(db, cuid)

    if user_res:
        print(user_res)
        return user_res
    else:
        print(3)
        raise credentials_exception


#print(get_current_user(access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbHpvMGhuZ3owMDAxOWgzcTI3MzUxaHl0IiwiZXhwIjoxNzIzMzczMjY0fQ.xaNC9NFYPDHaN8ydnZOcyipsG1XVXRAg1ayumaocRXk"))

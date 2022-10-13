import os
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

import crud
from RestModels.requestModels import TokenData
from util.dbCreator import get_db
from util.passwordManager import verify_password

# TODO 部署时候配置变量
SECRET_KEY = os.getenv("SECRET_KEY") if os.getenv("SECRET_KEY") \
    else "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    db_usr = crud.get_user_by_name(db, username)
    if not db_usr:
        return False
    if not verify_password(password, db_usr.password):
        return False
    return db_usr


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, db: Session):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_usr = crud.get_user_by_name(db, token_data.username)
    if not db_usr:
        raise credentials_exception
    return True

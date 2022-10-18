from typing import List

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# expiration_exception = HTTPException(
#     status_code=status.HTTP_403_FORBIDDEN,
#     detail="Token expired",
#     headers={"WWW-Authenticate": "Bearer"},
# )

login_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    detail: str


class CommitInRes(BaseModel):
    id: int = None
    time: str
    type: int
    name: str
    stu_id: str
    major: str
    instructor: str
    res: List[int]
    detail_res:str

class PageResponse(BaseModel):
    total: int
    data: List[CommitInRes]
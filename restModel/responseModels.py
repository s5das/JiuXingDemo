from typing import List

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class Message(BaseModel):
    msg: str


class CommitInRes(BaseModel):
    id: int = None
    time: str
    type: int
    name: str
    stu_id: str
    major: str
    instructor: str
    res: List[int]



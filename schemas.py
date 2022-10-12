from typing import List

from pydantic import BaseModel


class Commit(BaseModel):
    name: str
    stu_id: str
    major: str
    instructor: str
    res: List[int]


class CommitCreate(BaseModel):
    id: int = None
    time: str
    type: int
    name: str
    stu_id: str
    major: str
    instructor: str
    res: str


class CommitInExcel(BaseModel):
    time: str
    type: int
    name: str
    stu_id: str
    major: str
    instructor: str
    res: List[int]


class CommitResponse(Commit):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    password: str

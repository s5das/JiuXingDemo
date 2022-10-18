from typing import List

from pydantic import BaseModel, ValidationError, validator


class Commit(BaseModel):
    name: str
    stu_id: str
    major: str
    instructor: str
    res: List[int]
    detail_res:str


    @validator('stu_id')
    def stu_id_must_be_11_digits(cls, v):
        if len(v) != 11:
            raise ValueError('stu_id must be 12 digits')
        return v

    @validator('name', 'instructor')
    def name_must_be_2_to_10_chars(cls, v):
        if len(v) < 2 or len(v) > 10:
            raise ValueError('name must be 2 to 10 chars')
        return v

    @validator('major')
    def major_must_be_2_to_20_chars(cls, v):
        if len(v) < 2 or len(v) > 20:
            raise ValueError('major must be 2 to 20 chars')
        return v

    @validator('res')
    def res_must_be_9_ints(cls, v):
        if len(v) != 9:
            raise ValueError('res must be 9 ints')
        return v


class CommitCreate(BaseModel):
    id: int = None
    time: str
    type: int
    name: str
    stu_id: str
    major: str
    instructor: str
    res: str
    detail_res:str


class CommitInExcel(BaseModel):
    time: str
    type: int
    name: str
    stu_id: str
    major: str
    instructor: str
    res: List[int]


class User(BaseModel):
    name: str
    password: str

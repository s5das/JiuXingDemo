from sqlalchemy import Column, Integer, String
from sqlalchemy import SmallInteger

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    password = Column(String)


class Commit(Base):
    __tablename__ = "Commits"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(String)
    type = Column(SmallInteger)
    name = Column(String)
    stu_id = Column(String)
    major = Column(String)
    instructor = Column(String)
    res = Column(String)
    detail_res = Column(String)

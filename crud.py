from sqlalchemy.orm import Session

import models
import schemas
from util.convert import convert_commit_to_create
from util.passwordManager import get_password_hash


def create_user(db: Session, user: schemas.User):
    db_user = models.User(**user.dict())
    db_user.password = get_password_hash(db_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.__dict__


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_commits(db: Session, skip: int = 0, limit: int = 100, flag: bool = False):
    if flag:
        return db.query(models.Commit).all()
    return db.query(models.Commit).offset(skip).limit(limit).all()


def get_commit_by_id(db: Session, id: int):
    return db.query(models.Commit).filter(models.Commit.id == id).first()


def get_commit_by_stu_id(db: Session, stu_id: str):
    return db.query(models.Commit).filter(models.Commit.stu_id == stu_id).first()


def delete_commit_by_id(db: Session, commit_id: int):
    db.query(models.Commit).filter(models.Commit.id == commit_id).delete()
    db.commit()


def create_commit(db: Session, commit: schemas.Commit):
    commit_to_create = convert_commit_to_create(commit)
    db_commit = models.Commit(**commit_to_create.dict())
    db.add(db_commit)
    db.commit()
    db.refresh(db_commit)
    return db_commit.__dict__

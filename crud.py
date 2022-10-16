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
    return db_user


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_commits(db: Session):
    return db.query(models.Commit).all()


def get_commits_by_page(db: Session, page: int, page_size: int = 10):
    q2 = db.query(models.Commit).offset((page - 1) * page_size).limit(page_size)

    # sub = q1.subquery()
    q1 = db.query(models.Commit)
    cnt = (q1.count() + page_size - 1) // page_size
    return [cnt, q2.all()]


# def get_pages_cnt(db: Session, page_size: int = 10):
#     return (db.query(models.Commit).count() + page_size - 1) // page_size


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
    return db_commit


def query_commits_by_stu_id(db: Session, stu_id: str, page: int = 1, page_size: int = 10):
    q1 = db.query(models.Commit).filter(models.Commit.stu_id.like(stu_id + "%"))
    sub = q1.subquery()
    q2 = db.query(sub).offset((page - 1) * page_size).limit(page_size)
    cnt = (q1.count() + page_size - 1) // page_size
    return [cnt, q2.all()]


def query_commits_by_name(db: Session, name: str, page: int = 1, page_size: int = 10):
    q1 = db.query(models.Commit).filter(models.Commit.name.like(name + "%"))
    sub = q1.subquery()
    q2 = db.query(sub).offset((page - 1) * page_size).limit(page_size)
    cnt = (q1.count() + page_size - 1) // page_size
    return [cnt, q2.all()]


def query_commits_by_instructor(db: Session, instructor: str, page: int = 1, page_size: int = 10):
    q1 = db.query(models.Commit).filter(models.Commit.instructor.like(instructor + "%"))
    sub = q1.subquery()
    q2 = db.query(sub).limit((page - 1) * page_size).limit(page_size)
    cnt = (q1.count() + page_size - 1) // page_size
    return [cnt, q2.all()]


def query_commits_by_major(db: Session, major: str, page: int = 1, page_size: int = 10):
    q1 = db.query(models.Commit).filter(models.Commit.major.like(major + "%"))
    sub = q1.subquery()
    q2 = db.query(sub).limit((page - 1) * page_size).limit(page_size)
    cnt = (q1.count() + page_size - 1) // page_size
    return [cnt, q2.all()]

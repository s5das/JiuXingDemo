# from builtins import function
from typing import List

import models
import schemas
from database import engine
from restModel.responseModels import CommitInRes
from util.timeUtil import get_current_beijing_time

models.Base.metadata.create_all(bind=engine)


def convert_list_to_string(lst: List):
    return ','.join([str(i) for i in lst])


def convert_str_to_list(str: str):
    return [int(i) for i in str.split(',')]


def convert_commit_to_create(commit: schemas.Commit):
    cur_time = get_current_beijing_time()
    tmp_dict = commit.dict()
    tmp_dict['time'] = cur_time
    tmp_dict['type'] = commit.res.index(max(commit.res)) + 1
    # tmp_dict['res'] = ','.join([str(i) for i in commit.res])
    tmp_dict['res'] = convert_list_to_string(commit.res)
    return schemas.CommitCreate(**tmp_dict)


def convert_templete(db_res, func):
    return list(map(func, db_res))


def convert_db_commit_to_CommitCreate(db_commit: models.Commit):
    tmp_dict = db_commit.__dict__
    tmp_dict['res'] = convert_str_to_list(tmp_dict['res'])
    return schemas.CommitCreate(**tmp_dict)


def convert_db_commit_to_CommitInExcel(db_commit: models.Commit):
    tmp_dict = db_commit.__dict__
    tmp_dict['res'] = convert_str_to_list(tmp_dict['res'])
    return schemas.CommitInExcel(**tmp_dict)


def convert_db_commit_to_CommitResponse(db_commit: models.Commit):
    if type(db_commit) == dict:
        tmp_dict = db_commit
    else:
        tmp_dict = db_commit.__dict__
    tmp_dict['res'] = convert_str_to_list(tmp_dict['res'])
    # print (str(tmp_dict))
    return CommitInRes(**tmp_dict)


# def convert_data_to_page(db: Session, data: List, current_page_index: int, page_size: int):
#     # return data[(current_page_index - 1) * page_size:current_page_index * page_size]
#     pages_cnt = crud.get_pages_cnt(db)

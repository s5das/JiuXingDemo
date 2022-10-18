import os
from datetime import timedelta
from io import BytesIO
from typing import List, Union

from fastapi import Depends, FastAPI, HTTPException
from fastapi import Request, Query
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from openpyxl import Workbook
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

import crud
import restModel
import schemas
from restModel.responseModels import Token, login_exception
from util.convert import convert_templete, \
    convert_db_commit_to_CommitResponse
from util.dbCreator import get_db
from util.scheduleTask import MailSender
from util.tokenManager import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from util.tokenManager import authenticate_user, verify_access_token

limiter = Limiter(key_func=get_remote_address)
if os.getenv("ENV") == "dev":
    app = FastAPI(title="九型人格demo", description="demo接口文档", version="1.0.0")
else:
    app = FastAPI(title="九型人格demo", description="demo接口文档", version="1.0.0", openapi_url=None)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if os.getenv("MAIL_NAME"):
    mail_name = os.getenv("MAIL_NAME")
    mail_password = os.getenv("MAIL_PASSWORD")
    mail_host = os.getenv("MAIL_HOST")
    mail_port = os.getenv("MAIL_PORT")
    receiver = os.getenv("MAIL_RECEIVER")
    mailSender = MailSender(mail_name, mail_password, mail_host, mail_port, receiver)
    mailSender.create_task()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/commit",
          description='''提交测试结果,res为测试结果,
          例如：res = [1,2,3,...9] -> 代表一类得分为1，二类得分为2，三类得分为3，
          ...，九类得分为9, 接口返回分类 用于确定数据保存成功''',
          response_model=restModel.responseModels.CommitInRes,
          responses={400: {"description": "学号已存在 | 测试结果不能全为0 | 分类数组长度不为9",
                           "model": restModel.responseModels.Message},
                     # 500: {"description": "服务器错误", "model": restModel.responseModels.Message}
                     },
          tags=["学生"]
          )
# @limiter.limit("100/minute")
@limiter.limit("1000/hour")
@limiter.limit("5000/day")
def add_commit(request: Request, commit: schemas.Commit, db: Session = Depends(get_db)):
    db_commit = crud.get_commit_by_stu_id(db, commit.stu_id)
    if db_commit:
        raise HTTPException(status_code=400, detail="学号已存在")
    if max(commit.res) == 0:
        raise HTTPException(status_code=400, detail="测试结果不能全为0")
    res1 = crud.create_commit(db, commit)
    return convert_db_commit_to_CommitResponse(res1)


@app.post("/api/v1/addUser",
          description="用于开发时录入用户",
          response_model=restModel.responseModels.Message,
          responses={
              400: {"description": "操作失败", "model": restModel.responseModels.Message},
              401: {"description": "用户名已存在", "model": restModel.responseModels.Message},
              # 500: {"description": "服务器错误", "model": restModel.responseModels.Message},
          },

          tags=["dev"]
          )
def add_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    # exceptWrapper(crud.create_user, [db, user], "创建失败")
    crud.create_user(db, user)
    return {"detail": "创建成功"}


@app.post("/api/v1/login",
          description="登录接口，返回token",
          responses={
              401: {"description": "Incorrect username or password", "model": restModel.responseModels.Message},
              500: {"description": "服务器错误", "model": restModel.responseModels.Message},
          },
          response_model=Token,
          tags=["书院"])
@limiter.limit("30/minute")
def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    db_usr = authenticate_user(form_data.username, form_data.password, db)
    if not db_usr:
        raise login_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_usr.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/v1/queryAll",
         description="获取全部的提交结果",
         response_model=List[restModel.responseModels.CommitInRes],
         responses={
             401: {"description": "token错误", "model": restModel.responseModels.Message},
             # 500: {"description": "服务器错误", "model": restModel.responseModels.Message},
         },
         dependencies=[Depends(verify_access_token)],
         tags=["书院"])
def get_commits(db: Session = Depends(get_db)):
    res_list = crud.get_commits(db)
    # return exceptWrapper(convert_templete, [res_list, convert_db_commit_to_CommitResponse], "查询失败")
    return convert_templete(res_list, convert_db_commit_to_CommitResponse)


@app.get(
    "/api/v1/queryByPage",
    description="传入页码和每页长度(默认为10)，返回指定页码的数据, 数据长度需要自行判断",
    response_model=restModel.responseModels.PageResponse,
    # response_model_exclude=
    dependencies=[Depends(verify_access_token)],
    tags=["书院"])
def get_commits_by_page(page: int = Query(gt=1, default=1), page_size: int = 10, db: Session = Depends(get_db)):
    res_list = crud.get_commits_by_page(db, page, page_size)
    res_list[-1] = convert_templete(res_list[-1], convert_db_commit_to_CommitResponse)
    key = ["total", "data"]
    # res =  dict(zip(key, res_list))
    # print (res)
    return dict(zip(key, res_list))


# Union["学号", "姓名", "辅导员", "大类"]
@app.get("/api/v1/queryByFilter",
         description="传入筛选条件，返回符合条件的数据",
         # response_model=restModel.responseModels.PageResponse,
         dependencies=[Depends(verify_access_token)],
         tags=["书院"])
def get_commits_by_filter(arg: Union[str],
                          page: int = Query(gt=1, default=1),
                          filter_type: str = Query(regex="学号|姓名|辅导员|大类"),
                          db: Session = Depends(get_db)):
    # try:
    if filter_type == "学号":
        res_list = crud.query_commits_by_stu_id(db, arg, page)
    elif filter_type == "姓名":
        res_list = crud.query_commits_by_name(db, arg, page)
    elif filter_type == "辅导员":
        res_list = crud.query_commits_by_instructor(db, arg, page)
    else:
        res_list = crud.query_commits_by_major(db, arg, page)

    for i in range(len(res_list[-1])):
        res_list[-1][i] = res_list[-1][i]._asdict()

    res_list[-1] = convert_templete(res_list[-1], convert_db_commit_to_CommitResponse)

    key = ["total", "data"]
    return dict(zip(key, res_list))


@app.delete("/api/v1/deleteById",

            description="删除指定id的提交",
            response_model=restModel.responseModels.Message,
            responses={
                400: {"description": "id不存在", "model": restModel.responseModels.Message},
                401: {"description": "token错误", "model": restModel.responseModels.Message},
                500: {"description": "服务器错误", "model": restModel.responseModels.Message},
            },
            dependencies=[Depends(verify_access_token)],
            tags=["书院"])
def delete_commit(id: int, db: Session = Depends(get_db)):
    if not crud.get_commit_by_id(db, id):
        raise HTTPException(status_code=400, detail="id不存在")
    try:
        crud.delete_commit_by_id(db, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)
    return {"detail": "id " + str(id) + ": 删除成功"}


@app.get("/api/v1/queryById",
         description="查询接口，返回指定编号的提交的数据",
         response_model=restModel.responseModels.CommitInRes,
         responses={
             400: {"description": "id不存在", "model": restModel.responseModels.Message},
             401: {"description": "token错误", "model": restModel.responseModels.Message},
             # 500: {"description": "服务器错误", "model": restModel.responseModels.Message},
         },
         dependencies=[Depends(verify_access_token)],
         tags=["书院"])
def get_commit_by_id(id: int, db: Session = Depends(get_db)):
    if not crud.get_commit_by_id(db, id):
        raise HTTPException(status_code=400, detail="id不存在")
    # return exceptWrapper(convert_db_commit_to_CommitResponse, [crud.get_commit_by_id(db, id)], "查询失败")
    return convert_db_commit_to_CommitResponse(crud.get_commit_by_id(db, id))


@app.get("/api/v1/getExcel",
         description="返回excel文件",
         response_description="返回二进制文件",
         responses={
             401: {"description": "token错误", "model": restModel.responseModels.Message},
             # 403: {"description": "token过期", "model": restModel.responseModels.Message},
             500: {"description": "服务器错误", "model": restModel.responseModels.Message},
         },
         dependencies=[Depends(verify_access_token)],
         tags=["书院"])
def get_docs(db: Session = Depends(get_db)):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "results"
    excel_title = ["序号", '提交时间', '测试结果', '姓名', '学号', '大类', '辅导员姓名', '一类得分', '二类得分',
                   '三类得分', '四类得分', '五类得分', '六类得分', '七类得分', '八类得分', '九类得分']
    ws1.append(excel_title)

    item_name = ['id', 'time', 'type', 'name', 'stu_id', 'major', 'instructor']

    def get_item(commit: dict):
        item = []
        for i in item_name:
            item.append(commit[i])
        item.extend(list(map(int, commit['res'].split(','))))
        return item

    res_in_db = crud.get_commits(db)
    for index, idx in enumerate(range(len(res_in_db)), 1):
        res_in_db[idx].id = index

    for row in range(2, len(res_in_db) + 2):
        item_list = get_item(res_in_db[row - 2].__dict__)
        ws1.append(item_list)

    with BytesIO() as f:
        wb.save(f)
        return StreamingResponse(
            iter([f.getvalue()]),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=results.xlsx"}
        )

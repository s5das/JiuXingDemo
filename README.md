## 九型人格后端demo

> [需求文档](https://otkyd4jmkr.feishu.cn/docx/doxcn5tlhyN0pwtLfqG0e13mgyb)

### overview

1. 使用fastapi框架快速开发， 数据库使用sqlite
2. 简单实现crud, 利用框架自动生成接口文档 访问 localhost:8000/docs 查看
3. 采用官方推荐的方式， 认证部分使用Oauth2 + jwt<br>
    - login接口返回示例  <br>

```json
{
  "access_token": "xxx",
  "token_type": "bearer"
}
```

- query接口请求示例 <br>

```Curl
curl --location --request GET 'localhost:8000/api/v1/query' \
--header 'Authorization: Bearer TOKEN' \
--data-raw ''
```

4. api参考 assert目录下.json文件 [swagger editor](https://editor.swagger.io/)

### lanch

1. pip install -r requirements.txt
2. uvicorn main:app.py

## deployment

1. 添加环境变量 SECRET_KEY 用于生成 jwt token

> tips: openssl rand -hex 32

### TODO

1. 添加日志功能
2. 使用拦截器实现鉴权(目前是if判断)
3. jwt过期时间是否生效？
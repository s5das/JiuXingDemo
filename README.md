## 九型人格后端demo

> [需求文档](https://otkyd4jmkr.feishu.cn/docx/doxcn5tlhyN0pwtLfqG0e13mgyb)
>
> [接口文档](https://www.apifox.cn/apidoc/shared-a0d734ca-87c1-4e6c-9e6d-27f1b124da23)
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


### lanch

1. pip install -r requirements.txt
2. bash run.sh

## deployment

1. 添加环境变量 SECRET_KEY 用于生成 jwt token

> tips: openssl rand -hex 32

### TODO

1. [x] 添加日志功能
2. [x] 使用拦截器实现鉴权(目前是if判断)
3. [x] jwt过期时间是否生效 (jose库默认过期verify)
4. [x] status code added 
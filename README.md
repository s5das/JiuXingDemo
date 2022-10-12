## 九型人格后端demo

> [需求文档](https://otkyd4jmkr.feishu.cn/docx/doxcn5tlhyN0pwtLfqG0e13mgyb)

### overview

1. 使用fastapi框架快速开发， 数据库使用sqlite
2. 简单实现crud, 利用框架自动生成接口文档 访问 localhost:8000/docs 查看
3. 采用官方推荐的方式， 认证部分使用Oauth2 + jwt<br>
   login接口返回示例

 ```json
{
  "access_token": "xxx",
  "token_type": "bearer"
}
```

### lanch

1. pip install -r requirements.txt
2. uvicorn main:app.py

### TODO

1. 添加日志功能
2. 使用拦截器实现鉴权(目前是if判断)
3. jwt过期时间是否生效？
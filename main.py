import os

import uvicorn

# from app import app
if __name__ == "__main__":
    # 日志设置
    dir_log = "logs"
    path_log = os.path.join(dir_log, 'logs.log')
    # 路径，每日分割时间，是否异步记录，日志是否序列化，编码格式，最长保存日志时间
    # logger.add(path_log, rotation='0:00', enqueue=True, serialize=False, encoding="utf-8", retention="10 days")
    # logger.debug("服务器重启！")
    # logger.
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=False)

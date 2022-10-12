import datetime
import time

import pytz


def get_current_beijing_time():
    tz = pytz.timezone('Asia/Shanghai')  # 东八区
    t = datetime.datetime.fromtimestamp(int(time.time()), pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
    return t

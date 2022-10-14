# import datetime
from datetime import datetime
from datetime import timedelta

if __name__ == "__main__":
    deley = timedelta(minutes=30)
    cur = datetime.utcnow()
    ls = [cur.timestamp(), (cur + timedelta(minutes=30)).timestamp()]
    # ls = list(map(str, ls))
    # print (ls)
    # print(len(ls[0]), len((ls[1])))
    # print(deley)
    ls = list(map(int, ls))
    print(ls[0] < ls[1])
    for i in ls:
        print(i)

# from util.tokenManager import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
# , create_access_token
import sys

sys.path.append("..")
from util.tokenManager import create_access_token, ALGORITHM, SECRET_KEY
from jose import jwt

token = create_access_token(
    data={"sub": "ccds"}
)

payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
print(payload)

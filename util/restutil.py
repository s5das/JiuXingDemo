from typing import Callable, List

from fastapi.exceptions import HTTPException


def exceptWrapper(func: Callable, args: List, msg: str):
    try:
        return func(*args)
    except Exception as e:
        raise HTTPException(status_code=400, detail=msg)

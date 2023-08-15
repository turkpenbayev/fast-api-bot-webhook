from typing import List, Iterable

from fastapi import status
from fastapi.requests import Request
from fastapi.exceptions import HTTPException


async def authorize(request: Request):
    if request.scope['user'] is None or not request.scope['auth']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication credentials are not provided'
        )
    return

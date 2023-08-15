from datetime import datetime, timedelta
import typing

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from pydantic import ValidationError
import jwt

from app.config import settings
from app.auth.schemas import TokenPayload, User

reusable_auth = HTTPBearer()


def get_token_user(token: str = Depends(reusable_auth)) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)

    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not decode credentials",
        )

    return User(id=token_data.user_id, telegram_user_id=token_data.telegram_user_id)


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def user(request: Request) -> User:
    if request.scope['user'] is None or not request.scope['auth']:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Authentication credentials are not provided'
        )
    return request.scope['user']


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> User:
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")
            request.scope['auth'] = True
            request.scope['user'] = self.get_token_user(
                credentials.credentials)
            return request.scope['user']
        else:
            request.scope['auth'] = False
            request.scope['user'] = User.anonymous()
        return request.scope['user']

    def get_token_user(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[
                    settings.JWT_ALGORITHM]
            )
            token_data = TokenPayload(**payload)

        except ValidationError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        except jwt.DecodeError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not decode credentials",
            )

        return User(id=token_data.user_id, username=token_data.username, telegram_user_id=token_data.telegram_user_id)

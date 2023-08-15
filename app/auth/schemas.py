from typing import Optional, List

from pydantic import BaseModel


class TokenPayload(BaseModel):
    # type: str
    exp: int
    # jti: str
    user_id: int
    username: str
    telegram_user_id: Optional[str]


class User(BaseModel):
    id: Optional[int]
    username: Optional[str]
    telegram_user_id: Optional[str]

    @classmethod
    def anonymous(cls):
        return cls(id=None, username=None, telegram_user_id=None)

    @property
    def is_authenticated(self):
        return self.id is not None

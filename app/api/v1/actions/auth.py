from datetime import timedelta
import passlib

from pydantic import BaseModel
from app.api.v1.actions.base import ActionBase, ActionError
from app.api.v1.db_data import UserInDB
from app.auth.base import create_access_token
from app.config import settings


def get_action_token(user: UserInDB) -> str:
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "user_id": user.user_id,
            "username": user.username,
            "telegram_user_id": user.telegram_user_id
        }, expires_delta=access_token_expires
    )
    return access_token


class Login(ActionBase):
    class Model(BaseModel):
        access_token: str
        token_type: str

    def __call__(self, username: str, password: str) -> Model:
        user = self.db.get_user(username)
        if not user:
            raise ActionError('username not found')

        if not settings.PWD_CONTEXT.verify(password, user.password):
            raise ActionError('password not correct')

        access_token = get_action_token(user)
        return self.Model(access_token=access_token, token_type='bearer')


class Register(ActionBase):
    class Model(BaseModel):
        access_token: str
        token_type: str

    def __call__(self, username: str, password: str) -> Model:
        user_db = self.db.get_user(username)
        if user_db:
            raise ActionError("user registered")

        hashed_password = settings.PWD_CONTEXT.hash(password)
        user = self.db.create_user(username, hashed_password)
        access_token = get_action_token(user)
        return self.Model(access_token=access_token, token_type='bearer')
    

class SetUserTelegramID(ActionBase):
    def __call__(self, token: str, telegram_user_id: str) -> None:
        username = self.db.get_username_from_user_token(token)
        if username:
            self.db.set_telegram_user_id_to_user(username, telegram_user_id)

from datetime import datetime
import typing

from pydantic import BaseModel
from app.api.v1.actions.base import ActionBase, ActionError
from app.api.v1.db_data import UserMessagesInDB
from app.services.bot import send_telegram_message


class GetToken(ActionBase):
    class Model(BaseModel):
        token: str

    def __call__(self, username: str) -> Model:
        token = self.db.get_user_token(username)
        if token is None:
            raise ActionError('token not generated')
        return self.Model(token=token)


class GenerateToken(ActionBase):
    class Model(BaseModel):
        token: str

    def __call__(self, username: str) -> Model:
        token = self.db.generate_user_token(username)
        self.db.set_token_to_user(username, token)
        return self.Model(token=token)
    

class GetMessages(ActionBase):
    class Model(UserMessagesInDB):
        pass

    def __call__(self, username: str) -> typing.List[Model]:
        messages = self.db.get_user_messages(username)
        return [m for m in messages]
    

class CreateMessages(ActionBase):
    class Model(UserMessagesInDB):
        pass

    async def __call__(self, username: str, message: str) -> Model:
        user = self.db.get_user(username)
        formatted_message = f'{username}, я получил от тебя сообщение:\n{message}'
        user_message = self.db.create_user_message(username, message)
        if user.telegram_user_id:
            await send_telegram_message(user.telegram_user_id, formatted_message)
        return user_message
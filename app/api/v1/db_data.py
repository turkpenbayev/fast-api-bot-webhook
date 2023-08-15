from datetime import datetime
import typing
import secrets
from pydantic import BaseModel


class UserInDB(BaseModel):
    user_id: int
    username: str
    password: str
    token: str | None = None
    telegram_user_id: str | None = None


class UserMessagesInDB(BaseModel):
    message: str
    created_at: datetime


class Database:
    def __init__(self):
        self.start_user_id = 1
        self.users = {}
        self.messages = {}
        self.user_token = {}

    def create_user(self, username: str, password: str) -> UserInDB:
        user = UserInDB(
            username=username, password=password, user_id=self.start_user_id
        )
        self.users[username] = user
        self.generate_user_token(username)
        self.start_user_id += 1
        return user

    def get_user(self, username: str) -> UserInDB | None:
        return self.users.get(username)

    def generate_user_token(self, username: str) -> str:
        token = self.get_secret_token()
        self.user_token[token] = username
        return token
    
    def set_token_to_user(self, username, token) -> None:
        user = self.get_user(username)
        user.token = token
    
    def get_user_token(self, username: str) -> str | None:
        user = self.get_user(username)
        return user.token

    def set_telegram_user_id_to_user(self, username: str, telegram_user_id: str) -> None:
        user = self.get_user(username)
        user.telegram_user_id = telegram_user_id

    def get_username_from_user_token(self, token: str) -> str | None:
        return self.user_token.get(token)

    def create_user_message(self, username: str, message: str) -> UserMessagesInDB:
        messages = self.get_user_messages(username)
        user_message = UserMessagesInDB(
            message=message, created_at=datetime.now())
        messages.append(user_message)
        self.messages[username] = messages
        return user_message

    def get_user_messages(self, username: str) -> typing.List[UserMessagesInDB]:
        return self.messages.get(username, [])

    def get_secret_token(self) -> str:
        return secrets.token_hex(8)


database = Database()


def get_database():
    return database

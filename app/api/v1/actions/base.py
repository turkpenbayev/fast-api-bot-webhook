from fastapi import HTTPException
from starlette import status
from app.api.v1.db_data import Database


class ActionBase:
    def __init__(self, db: Database):
        self.db = db

    def __call__(self, *args, **kwargs):
        pass


class ActionError(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'action_error'
    default_detail = 'Can not perform action.'

    def __init__(self, detail=None, status_code=None, code=None):
        if detail is None:
            detail = self.default_detail
        if status_code is None:
            status_code = self.status_code
        if code is None:
            code = self.default_code

        self.detail = str(detail)
        self.code = code
        self.status_code = status_code

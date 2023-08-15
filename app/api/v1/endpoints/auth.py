from fastapi import APIRouter, Depends, Request, Response

from app.api.v1.actions import auth
from app.api.v1.db_data import Database, get_database

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post("/register/", response_model=auth.Register.Model)
def register(username: str, password: str, db: Database = Depends(get_database)):
    return auth.Register(db)(username, password)


@router.post("/login/", response_model=auth.Login.Model)
def login(username: str, password: str, db: Database = Depends(get_database)):
    return auth.Login(db)(username, password)


@router.post("/webhook/")
async def webhook(req: Request, db: Database = Depends(get_database)):
    data = await req.json()
    token = data['message']['text']
    chat_id = data['message']['chat']['id']
    auth.SetUserTelegramID(db)(token=token, telegram_user_id=chat_id)
    return Response(status_code=200)
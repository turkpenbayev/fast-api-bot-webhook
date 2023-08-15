from typing import List
import typing

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.db_data import Database, get_database

from app.auth.base import JWTBearer, user
from app.auth.schemas import User
from app.auth.permissions import authorize
from app.api.v1.actions import user as fab_user
from app.db import get_db

router = APIRouter(
    dependencies=[
        Depends(JWTBearer()),
        Depends(authorize),
    ],
    tags=['users']
)


@router.get('/token/', response_model=fab_user.GetToken.Model)
def get_token(
    user: User = Depends(user),
    db: Database = Depends(get_database)
):
    return fab_user.GetToken(db)(user.username)


@router.post('/token/', response_model=fab_user.GetToken.Model)
def generate_token(
    user: User = Depends(user),
    db: Database = Depends(get_database)
):
    return fab_user.GenerateToken(db)(user.username)


@router.get('/messages/', response_model=typing.List[fab_user.GetMessages.Model])
def get_messages(
    user: User = Depends(user),
    db: Database = Depends(get_database)
):
    return fab_user.GetMessages(db)(user.username)


@router.post('/messages/', response_model=fab_user.CreateMessages.Model)
async def create_messages(
    message: str,
    user: User = Depends(user),
    db: Database = Depends(get_database)
):
    return await fab_user.CreateMessages(db)(user.username, message=message)

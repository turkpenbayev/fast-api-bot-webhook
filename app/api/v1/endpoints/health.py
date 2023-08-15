from fastapi import APIRouter, Response, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix='/health', tags=['health'])


@router.get('/alive/')
def alive():
    return Response(status_code=200)


@router.get('/ready/')
def ready(db: Session = Depends(get_db)):
    db.execute('select 1')
    return Response(status_code=200)


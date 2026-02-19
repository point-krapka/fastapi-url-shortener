from fastapi import APIRouter,Body,Depends,HTTPException
from app.infrastructure.db.database import get_db
from app.application.user.model import UserRegister
from typing import Annotated
from app.application.user.auth import create_user,login_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.error import NotFoundError,AlreadyExistsError,IncorrectPassword
router = APIRouter(prefix='/api',tags=['user'])



@router.post('/register/')
async def register(
                   db: Annotated[AsyncSession, Depends(get_db)], 
                   user:Annotated[UserRegister,Body()]):
    try:
        await create_user(db,user)
    except AlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.post('/login/')
async def login(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[UserRegister, Body()]
):
    try:
        return await login_user(db, user)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.message)
    except IncorrectPassword as e:
        raise HTTPException(status_code=401, detail=e.message)

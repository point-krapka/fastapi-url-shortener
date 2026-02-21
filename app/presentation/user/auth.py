from fastapi import APIRouter,Body,Depends,HTTPException,Response
from app.infrastructure.db.database import get_db
from app.application.user.model import UserRegister
from typing import Annotated
from app.application.user.model import UserResponse
from app.application.user.auth import create_user,login_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.security import create_access_token
from app.infrastructure.error import NotFoundError,AlreadyExistsError,IncorrectPassword
router = APIRouter(prefix='/api',tags=['user'])



@router.post('/register/')
async def register(
                   db: Annotated[AsyncSession, Depends(get_db)], 
                   user:Annotated[UserRegister,Body()],
                   response: Response):
    try:
        user:UserResponse = await create_user(db,user)
        response.set_cookie(key="access_token",value=create_access_token(user.id))
        return user
    except AlreadyExistsError:
        raise HTTPException(status_code=409, detail="Login taken")


@router.post('/login/')
async def login(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[UserRegister, Body()],
    response: Response
):
    try:
        user:UserResponse = await login_user(db, user)
        response.set_cookie(key="access_token",value=create_access_token(user.id))
        return user

    except (NotFoundError, IncorrectPassword):
        raise HTTPException(status_code=401, detail="Incorect login or password")

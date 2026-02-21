from fastapi import APIRouter,Body,Depends,HTTPException,Response
from app.infrastructure.db.database import get_db
from typing import Annotated
from app.application.site.create_link import create_link
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.security import get_current_user
from app.application.site.model import LinkCreate,LinkResponse
from app.infrastructure.error import NotFoundError,AlreadyExistsError,IncorrectPassword

router = APIRouter(prefix='/api',tags=['link'])
@router.post("/create_link",status_code=201,
    responses={
    201: {"description": "Link successfully created"},
    401: {"description": "Unauthorized"},
    409: {"description": "Failed to generate unique short_url"},
    422: {"description": "Validation error"},
},)
async def api_create_link(
                   db: Annotated[AsyncSession, Depends(get_db)], 
                   link:Annotated[LinkCreate,Body()],
                   user=Depends(get_current_user)) -> LinkResponse:
    try:
        return await create_link(db,user_id=user['sub'],origin_url=str(link.origin_url))
    except RuntimeError:
        raise HTTPException(status_code=409,
         detail="Unable to generate unique short_url. Please try again later.")
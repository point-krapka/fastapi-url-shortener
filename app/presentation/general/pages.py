from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from pathlib import Path

from app.infrastructure.db.database import get_db
from app.infrastructure.db.repo.link import get_link_by_short_url
from app.infrastructure.error import NotFoundError

router = APIRouter(tags=['general'])
templates_path = Path('app', 'presentation', 'static', 'html')
favicon_path = Path('app', 'presentation', 'static', 'img', 'favicon.ico')
templates = Jinja2Templates(directory=templates_path)


@router.get('/')
async def home(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')


@router.get('/register')
async def register(request: Request):
    return templates.TemplateResponse(request=request, name='register.html')


@router.get('/login')
async def login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')


@router.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@router.get('/{short_url}')
async def redirect_page(
    short_url: str,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    try:
        link = await get_link_by_short_url(db, short_url)
    except NotFoundError:
        raise HTTPException(status_code=404, detail='Short link not found')

    return templates.TemplateResponse(
        request=request,
        name='redirect.html',
        context={'target_url': link.origin_url, 'short_url': short_url},
    )

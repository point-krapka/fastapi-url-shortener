from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.infrastructure.db.database import engine
from app.infrastructure.db.models.base import Base
from contextlib import asynccontextmanager
from app.presentation.user import auth
from app.presentation.general import pages
from app.presentation.site import create_link
from app.presentation.site import manage_link
from app.presentation.visit import track
from app.infrastructure.db.models.base import Base
from app.infrastructure.db.models.user import User
from app.infrastructure.db.models.link import Link
from app.infrastructure.db.models.visit import Visit
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

path_static = os.path.join("app","presentation","static")
app.mount("/static", StaticFiles(directory=path_static), name="static")
templates = Jinja2Templates(directory=os.path.join(path_static, "html"))


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request, name="404.html", status_code=404
        )
    if exc.status_code == 401:
        return templates.TemplateResponse(request=request,
        status_code=401,name="register.html")
    if exc.status_code == 403:
        return templates.TemplateResponse(
            request=request, name="403.html", status_code=403
        )
    if 500 <= exc.status_code <= 599:
        return templates.TemplateResponse(
            request=request, name="5xx.html", status_code=exc.status_code
        )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.exception_handler(Exception)
async def custom_server_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse(request=request, name="5xx.html", status_code=500)


app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(create_link.router)
app.include_router(manage_link.router)
app.include_router(track.router)

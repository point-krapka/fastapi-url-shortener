from fastapi import FastAPI
from app.infrastructure.db.database import engine
from app.infrastructure.db.models.base import Base
from contextlib import asynccontextmanager
from app.presentation.user import auth
from app.presentation.general import pages
from app.presentation.site import create_link
from app.infrastructure.db.models.base import Base
from app.infrastructure.db.models.user import User
from app.infrastructure.db.models.link import Link
from app.infrastructure.db.models.visit import Visit
from fastapi.staticfiles import StaticFiles
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

path_static = os.path.join("app","presentation","static")
app.mount("/static", StaticFiles(directory=path_static), name="static")


app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(create_link.router)
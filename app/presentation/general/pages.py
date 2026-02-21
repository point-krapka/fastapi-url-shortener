from fastapi import APIRouter,Depends,Request
from app.infrastructure.security import get_current_user
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
router = APIRouter(tags=['general'])
templates_path = Path("app","presentation","static","html")
favicon_path = Path("app","presentation","static","img","favicon.ico")
templates = Jinja2Templates(directory=templates_path)

@router.get("/")
async def home(payload=Depends(get_current_user)):
    return {"payload":payload}


@router.get("/register")
async def register(request:Request):
    return templates.TemplateResponse(request=request, name="register.html")



@router.get("/login")
async def register(request:Request):
   return templates.TemplateResponse(request=request, name="login.html")




@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
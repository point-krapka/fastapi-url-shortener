from fastapi import APIRouter,Depends
from app.infrastructure.security import get_current_user
router = APIRouter(tags=['general'])

@router.get("/")
async def home(payload=Depends(get_current_user)):
    return {"payload":payload}
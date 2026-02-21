from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.visit.model import  VisitTrackRequest
from app.infrastructure.db.database import get_db
from app.infrastructure.db.models.visit import Visit
from app.infrastructure.db.repo.link import get_link_by_short_url
from app.infrastructure.error import NotFoundError
from app.application.visit.track import register_track_visit
router = APIRouter(prefix="/api", tags=["visit"])


@router.post("/track", status_code=204)
async def track_visit(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    track_data: Annotated[VisitTrackRequest, Body()],
):
    await register_track_visit(db,track_data,request)

    return Response(status_code=204)

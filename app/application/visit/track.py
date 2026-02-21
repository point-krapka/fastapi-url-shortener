from fastapi import Depends,Request,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models.user import User
from app.infrastructure.db.repo.user import db_create_user,get_user_by_login
from bcrypt import gensalt, hashpw,checkpw
from app.infrastructure.error import NotFoundError,IncorrectPassword
from app.infrastructure.db.repo.link import get_link_by_short_url
from app.application.visit.model import VisitTrackRequest
from app.infrastructure.db.models.visit import Visit



async def register_track_visit(db:AsyncSession,track_data:VisitTrackRequest,
request:Request):
    try:
            link = await get_link_by_short_url(db, track_data.curl_url)
    except NotFoundError:
            raise HTTPException(status_code=404, detail="Short link not found")


    visit = Visit(
            ip_address = request.client.host,
            user_agent=request.headers.get("user-agent"),
            os=track_data.os,
            browser=track_data.browser,
            device=track_data.device,
            language=track_data.language,
            timezone=track_data.timezone,
            size_window=track_data.size_window,
            link_id=link.id,
        )
    link.count_visits += 1
    db.add(visit)
    await db.commit()

from pydantic import BaseModel,AnyHttpUrl
from app.application.visit import VisitBase
from datetime import datetime
class LinkResponse(BaseModel):
    id: int
    short_url: str
    origin_url: AnyHttpUrl
    count_visits: int
    created_at: datetime


class LinkCreate(BaseModel):
    origin_url: AnyHttpUrl

class AllVisitLink(LinkResponse):
    visits: list[VisitBase]
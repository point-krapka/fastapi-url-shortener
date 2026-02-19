from pydantic import BaseModel
from app.application.visit import VisitBase
from datetime import datetime
class LinkResponse(BaseModel):
    id: int
    short_url: str
    origin_url: str
    count_visits: int
    created_at: datetime


class LinkCreate(BaseModel):
    origin_url: str

class AllVisitLink(LinkResponse):
    visits: list[VisitBase]
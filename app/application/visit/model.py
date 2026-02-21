from pydantic import BaseModel
from datetime import datetime
class VisitBase(BaseModel):
    user_agent :str|None = None
    ip_address: str |None = None
    os: str|None = None
    browser: str|None = None
    device: str|None = None
    language:str|None = None
    timezone:str|None = None
    size_window: str|None = None
class VisitTrackRequest(VisitBase):
    curl_url :str

class VisitResponse(VisitBase):
    visit_id:int
    site_id: int
    created_at:datetime
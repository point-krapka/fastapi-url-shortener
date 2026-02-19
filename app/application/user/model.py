from pydantic import BaseModel
from datetime import datetime
class UserRegister(BaseModel):
    login: str
    password: str
    #Хардкорим is_admin:bool

    

class UserResponse(BaseModel):
    id: int
    login: str
    is_admin:bool
    created_at:datetime

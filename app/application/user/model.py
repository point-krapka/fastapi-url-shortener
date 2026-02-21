from pydantic import BaseModel,Field
from datetime import datetime
class UserRegister(BaseModel):
    login: str = Field(
        min_length=5,
        max_length=16,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="Only ASCII letters, digits and underscore"
    )
    password: str = Field(
        min_length=5,
        max_length=16,
        pattern=r'^[a-zA-Z0-9_]+$',
        description="Only ASCII letters, digits and underscore"
    )
    #Хардкорим is_admin:bool

    

class UserResponse(BaseModel):
    id: int
    login: str
    is_admin:bool
    created_at:datetime

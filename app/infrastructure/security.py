import jwt
from datetime import datetime,timezone,timedelta
from config.config.settings import settings
from fastapi import HTTPException, status,Depends,Request
from fastapi.security import OAuth2PasswordBearer


def create_access_token(user_id: int) -> str:
    payload = {
        
        "sub": str(user_id), 
        "iat": datetime.now(timezone.utc), 
    }

    return jwt.encode(payload,
        settings.SECRET_KEY_JWT,
        algorithm=settings.ALGORITHM_JWT)




def decode_jwt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_JWT,
                             algorithms=[settings.ALGORITHM_JWT])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    
def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=[settings.ALGORITHM_JWT])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
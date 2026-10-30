from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from security.encryption import get_secret,get_algorithm
from schemas import user_auth_scheme
import jwt



def authenticate_user(credentials: HTTPAuthorizationCredentials | None = Depends(user_auth_scheme)):
    if not credentials is None:
        try:
            payload = jwt.decode(credentials.credentials,get_secret(),get_algorithm())
        except:
            raise HTTPException(status_code=401)
    else:
        raise HTTPException(status_code=401)
    id = int(payload['sub'])
    return id
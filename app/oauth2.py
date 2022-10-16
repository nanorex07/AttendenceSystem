from datetime import timedelta, datetime
from jose import JWTError, jwt
from app.utils import jsonToBson
from .database import community_db
from .schemas.schemas import TokenData
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from .utils import jsonToBson
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    ret = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return ret


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Can not verify credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exceptions)
    user = await community_db.find_one({"_id": jsonToBson(token.id)})
    return user

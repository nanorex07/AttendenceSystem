from fastapi import APIRouter, Depends, status, HTTPException
from ..database import community_db
from ..schemas.schemas import Token
from .. import utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/api/login", response_model=Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends()):

    user = await community_db.find_one({"email": credentials.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    user["_id"] = utils.bsonToJson(user["_id"])
    access_token = oauth2.create_access_token(data={"user_id": user["_id"]})

    return {"access_token": access_token, "token_type": "bearer"}

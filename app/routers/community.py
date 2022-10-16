from colorama import Back
from .. import utils
from fastapi import HTTPException, status, Depends, APIRouter, BackgroundTasks
from ..schemas.schemas import CommunityOut, CommunityCreate
from ..database import community_db
from datetime import datetime
from typing import List
from .. import oauth2

router = APIRouter(prefix="/api/community", tags=["Community"])


def create_encoding_file(name: str):
    file = open(f"./face_encodings/{name}.pkl", "w")
    file.close()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CommunityOut)
async def add_community(community: CommunityCreate, bt: BackgroundTasks):
    exists = await community_db.find_one({"email": community.email})
    if exists:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="User with that email already exists.",
        )
    new_user = community.dict()
    new_user["created_at"] = datetime.utcnow()
    new_user["password"] = utils.hash(new_user["password"])
    res = await community_db.insert_one(new_user)
    bt.add_task(create_encoding_file, community.name)
    return new_user


@router.get("/", response_model=List[CommunityOut])
async def get_communities(current_user: int = Depends(oauth2.get_current_user)):
    listout = []
    cluster = community_db.find({})
    async for doc in cluster:
        listout.append(doc)
    return listout

from fastapi import Depends, APIRouter, File, UploadFile, HTTPException, status
from ..schemas.member import MemberCreate, MemberOut
from ..database import member_db, records_db
from ..face_utils.face_find import add_file, predict

from .. import oauth2
from ..utils import bsonToJson
from typing import List

from datetime import datetime

router = APIRouter(prefix="/api/members", tags=["Members"])


@router.get("/", response_model=List[MemberOut])
async def get_members(current_user: int = Depends(oauth2.get_current_user)):
    listout = []
    cluster = member_db.find({"community_id": bsonToJson(current_user["_id"])})
    async for doc in cluster:
        listout.append(doc)
    return listout


@router.post("/")
async def add_member(
    member: MemberCreate,
    current_user: int = Depends(oauth2.get_current_user),
):
    td = member.dict()
    st = str(bsonToJson(current_user.get("_id")))
    td["community_id"] = st
    td["image_added"] = False

    td = MemberOut(**td).dict()
    res = await member_db.insert_one(td)
    return True


@router.post("/add_image")
async def add_image(
    id: str,
    file: UploadFile = File(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    res = await member_db.find_one({"id": id})
    if not res:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="member not found"
        )
    bytes = await file.read()
    add_file(bytes, id, current_user.get("name"))
    res = await member_db.update_one({"id": id}, {"$set": {"image_added": True}})
    return True


@router.post("/mark")
async def mark_attendance(
    file: UploadFile = File(...),
    current_user: int = Depends(oauth2.get_current_user),
):
    bytes = await file.read()
    res = predict(bytes, current_user.get("name"))
    if len(res) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Can't recognize face, please check if face is added or not",
        )
    date = str(datetime.utcnow().date())
    ids = bsonToJson(current_user.get("_id"))
    res = await records_db.update_one(
        filter={
            "community_id": ids,
            "date": date,
        },
        update={
            "$set": {"community_id": ids, "date": date},
            "$addToSet": {"present": {"$each": res}},
        },
        upsert=True,
    )
    return res.modified_count > 0 or res.upserted_id

from operator import length_hint
from fastapi import Depends, APIRouter
from typing import List
from ..database import records_db
from ..utils import bsonToJson

from .. import oauth2

router = APIRouter(prefix="/api/records", tags=["Records"])


@router.get("/")
async def get_all_records(current_user: int = Depends(oauth2.get_current_user)):
    cluster = records_db.find({"community_id": bsonToJson(current_user["_id"])})
    ret = []
    async for c in cluster:
        del c["_id"]
        ret.append(c)
    return ret

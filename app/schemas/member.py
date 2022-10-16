from pydantic import BaseModel, root_validator
from datetime import datetime
from typing import Optional, Dict, Any


class MemberCreate(BaseModel):
    name: str
    id: str

    class Config:
        orm_mode = True


class MemberOut(BaseModel):
    # created_at: datetime
    name: str
    id: str
    community_id: str
    image_added: bool

    class Config:
        orm_mode = True

import motor.motor_asyncio
from .config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)

db = client[settings.db_name]
community_db = db.community
member_db = db.members
records_db = db.records

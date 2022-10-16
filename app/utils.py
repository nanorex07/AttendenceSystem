from passlib.context import CryptContext
from bson import json_util, ObjectId
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain, hashed):
    return pwd_context.verify(plain, hashed)

def bsonToJson(id: ObjectId):
    tid = json.loads(json_util.dumps(id))
    return tid["$oid"]

def jsonToBson(id: str):
    return ObjectId(oid=id)
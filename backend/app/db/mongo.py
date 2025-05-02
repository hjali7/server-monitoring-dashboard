from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URL, DATABASE_NAME

def get_client():
    return AsyncIOMotorClient(MONGO_URL)

def get_db():
    client = get_client()
    return client[DATABASE_NAME]
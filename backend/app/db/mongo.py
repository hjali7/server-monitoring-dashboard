from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Request

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "server_monitoring"

def get_client():
    return AsyncIOMotorClient(MONGO_URL)

def get_db():
    client = get_client()
    return client[DB_NAME]
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId, errors as bson_errors
import motor.motor_asyncio
import os
from dotenv import load_dotenv

# برای خواندن .env هنگام اجرای مستقیم
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DBNAME", "serverdb")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION", "servers")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
servers_collection = db[COLLECTION_NAME]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ServerBase(BaseModel):
    name: str
    ip: str
    status: str

class ServerInDB(ServerBase):
    id: str = Field(default_factory=str, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@app.get("/api/servers", response_model=List[ServerInDB])
async def get_servers():
    servers = []
    async for server in servers_collection.find():
        server["_id"] = str(server["_id"])
        servers.append(ServerInDB(**server))
    return servers

@app.post("/api/servers", response_model=ServerInDB)
async def add_server(server: ServerBase):
    server_dict = server.dict()
    result = await servers_collection.insert_one(server_dict)
    server_dict["_id"] = str(result.inserted_id)
    return ServerInDB(**server_dict)

@app.put("/api/servers/{server_id}", response_model=ServerInDB)
async def update_server(server_id: str, server: ServerBase):
    try:
        oid = ObjectId(server_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="شناسه سرور معتبر نیست")
    result = await servers_collection.update_one(
        {"_id": oid},
        {"$set": server.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="سرور پیدا نشد")
    updated_server = await servers_collection.find_one({"_id": oid})
    updated_server["_id"] = str(updated_server["_id"])
    return ServerInDB(**updated_server)

@app.delete("/api/servers/{server_id}", response_model=dict)
async def delete_server(server_id: str):
    try:
        oid = ObjectId(server_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="شناسه سرور معتبر نیست")
    result = await servers_collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="سرور پیدا نشد")
    return {"ok": True}
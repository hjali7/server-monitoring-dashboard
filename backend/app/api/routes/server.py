from fastapi import APIRouter, HTTPException, status
from app.models.server import ServerModel
from app.db.mongo import get_db
from bson import ObjectId

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.post("/", response_model=ServerModel, status_code=status.HTTP_201_CREATED)
async def create_server(server: ServerModel):
    db = get_db()
    data = server.dict(by_alias=True, exclude={"id"})
    result = await db.servers.insert_one(data)
    data["_id"] = str(result.inserted_id)
    return data

@router.get("/", response_model=list[ServerModel])
async def list_servers():
    db = get_db()
    servers = []
    async for s in db.servers.find():
        s["_id"] = str(s["_id"])
        servers.append(s)
    return servers

@router.get("/{server_id}", response_model=ServerModel)
async def get_server(server_id: str):
    db = get_db()
    server = await db.servers.find_one({"_id": ObjectId(server_id)})
    if server:
        server["_id"] = str(server["_id"])
        return server
    raise HTTPException(status_code=404, detail="Server not found")

@router.put("/{server_id}", response_model=ServerModel)
async def update_server(server_id: str, updated: ServerModel):
    db = get_db()
    data = updated.dict(by_alias=True, exclude_unset=True, exclude={"id"})
    result = await db.servers.update_one({"_id": ObjectId(server_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    server = await db.servers.find_one({"_id": ObjectId(server_id)})
    server["_id"] = str(server["_id"])
    return server

@router.delete("/{server_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_server(server_id: str):
    db = get_db()
    result = await db.servers.delete_one({"_id": ObjectId(server_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
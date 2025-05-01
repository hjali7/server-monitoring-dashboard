from fastapi import APIRouter, HTTPException, status
from app.models.server import ServerModel
from app.db.mongo import get_db
from bson.objectid import ObjectId

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
from fastapi import APIRouter, HTTPException
from app.db.mongo import get_db
from app.utils.ping import ping
from app.models.server_status import ServerStatusModel
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/status", tags=["Status"])

@router.post("/check-all")
async def check_status_all_servers():
    db = get_db()
    servers = []
    async for s in db.servers.find():
        servers.append(s)
    results = []
    for s in servers:
        is_online = await ping(s["ip"])
        status_doc = {
            "server_id": str(s["_id"]),
            "ip": s["ip"],
            "online": is_online,
            "checked_at": datetime.utcnow()
        }
        await db.server_status.insert_one(status_doc)
        results.append(status_doc)
    return results

@router.get("/history/{server_id}", response_model=list[ServerStatusModel])
async def history(server_id: str, limit: int = 20):
    db = get_db()
    cursor = db.server_status.find({"server_id": server_id}).sort("checked_at", -1).limit(limit)
    history = []
    async for h in cursor:
        h["_id"] = str(h["_id"])
        history.append(h)
    return history
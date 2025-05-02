from fastapi import APIRouter, Query, Depends
from app.db.mongo import get_db
from typing import List, Optional, Any
from bson import ObjectId

router = APIRouter(prefix="/server-status", tags=["Server Status"])

@router.get("/latest")
async def get_latest_status(
    tag: Optional[str] = Query(None),
    online: Optional[bool] = Query(None)
) -> List[Any]:
    db = get_db()
    query = {}
    if tag:
        query["tags"] = tag
    servers_cursor = db.servers.find(query)
    servers = []
    async for s in servers_cursor:
        s["_id"] = str(s["_id"])
        last_status = await db.server_status.find_one(
            {"server_id": s["_id"]},
            sort=[("checked_at", -1)]
        )
        if last_status:
            s["last_status"] = {
                "online": last_status["online"],
                "checked_at": last_status["checked_at"]
            }
        else:
            s["last_status"] = None
        servers.append(s)
    # فیلتر آنلاین/آفلاین
    if online is not None:
        servers = [srv for srv in servers if srv["last_status"] and srv["last_status"]["online"] == online]
    return servers
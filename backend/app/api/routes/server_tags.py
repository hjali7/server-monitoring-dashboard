from fastapi import APIRouter, HTTPException, status
from app.db.mongo import get_db
from bson import ObjectId

router = APIRouter(prefix="/servers", tags=["Server Tags"])

@router.post("/{server_id}/tags", status_code=200)
async def add_tag(server_id: str, tag: str):
    db = get_db()
    result = await db.servers.update_one(
        {"_id": ObjectId(server_id)},
        {"$addToSet": {"tags": tag}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"msg": "Tag added."}

@router.delete("/{server_id}/tags", status_code=200)
async def remove_tag(server_id: str, tag: str):
    db = get_db()
    result = await db.servers.update_one(
        {"_id": ObjectId(server_id)},
        {"$pull": {"tags": tag}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"msg": "Tag removed."}
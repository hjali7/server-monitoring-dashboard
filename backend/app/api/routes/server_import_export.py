from fastapi import APIRouter, UploadFile, File, Response, HTTPException
from app.db.mongo import get_db
import csv
import io
import json
from bson import ObjectId

router = APIRouter(prefix="/servers", tags=["Import/Export"])

@router.post("/import/csv")
async def import_servers_csv(file: UploadFile = File(...)):
    db = get_db()
    content = await file.read()
    csvfile = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        doc = {
            "name": row["name"].strip(),
            "ip": row["ip"].strip(),
            "description": row.get("description", "").strip(),
            "tags": [tag.strip() for tag in row.get("tags", "").split(",") if tag.strip()]
        }
        await db.servers.insert_one(doc)
        count += 1
    return {"msg": f"{count} servers imported."}

@router.post("/import/json")
async def import_servers_json(file: UploadFile = File(...)):
    db = get_db()
    content = await file.read()
    try:
        servers = json.loads(content)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    count = 0
    for s in servers:
        # حذف id قبلی در صورت وجود
        s.pop("_id", None)
        await db.servers.insert_one(s)
        count += 1
    return {"msg": f"{count} servers imported."}

@router.get("/export/csv")
async def export_servers_csv():
    db = get_db()
    servers = []
    async for s in db.servers.find():
        servers.append({
            "name": s["name"],
            "ip": s["ip"],
            "description": s.get("description", ""),
            "tags": ",".join(s.get("tags", []))
        })
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["name", "ip", "description", "tags"])
    writer.writeheader()
    for s in servers:
        writer.writerow(s)
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=servers.csv"})

@router.get("/export/json")
async def export_servers_json():
    db = get_db()
    servers = []
    async for s in db.servers.find():
        s["_id"] = str(s["_id"])
        servers.append(s)
    return servers
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.db.mongo import get_db
from app.utils.ping import ping
from datetime import datetime

async def check_all_servers_and_save():
    db = get_db()
    servers = []
    async for s in db.servers.find():
        servers.append(s)
    for s in servers:
        is_online = await ping(s["ip"])
        status_doc = {
            "server_id": str(s["_id"]),
            "ip": s["ip"],
            "online": is_online,
            "checked_at": datetime.utcnow()
        }
        await db.server_status.insert_one(status_doc)

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_all_servers_and_save, "interval", minutes=5)
    scheduler.start()
from fastapi import FastAPI
from app.api.routes import server, server_status
from app.scheduler import start_scheduler

app = FastAPI(
    title="Server Monitoring Dashboard",
    description="Backend API for monitoring and managing servers.",
    version="1.0.0"
)

app.include_router(server.router)
app.include_router(server_status.router)

@app.on_event("startup")
async def on_startup():
    start_scheduler()

@app.get("/")
def read_root():
    return {"msg": "Server Monitoring Dashboard Backend is running."}
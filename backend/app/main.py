from fastapi import FastAPI
from app.api.routes import server

app = FastAPI(
    title="Server Monitoring Dashboard",
    description="Backend API for monitoring and managing servers.",
    version="1.0.0"
)

app.include_router(server.router)

@app.get("/")
def read_root():
    return {"msg": "Server Monitoring Dashboard Backend is running."}
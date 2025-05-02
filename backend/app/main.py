from fastapi import FastAPI
from app.api.routes import server, server_status, auth

app = FastAPI(
    title="Server Monitoring Dashboard",
    description="Backend API for monitoring and managing servers.",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(server.router)
app.include_router(server_status.router)
from fastapi import FastAPI
from app.api.routes import server, server_status, server_tags, server_import_export

app = FastAPI(
    title="Server Monitoring Dashboard",
    description="Backend API for monitoring and managing servers.",
    version="1.0.0"
)

app.include_router(server.router)
app.include_router(server_status.router)
app.include_router(server_tags.router)
app.include_router(server_import_export.router)
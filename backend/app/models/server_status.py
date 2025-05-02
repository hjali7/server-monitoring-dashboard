from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ServerStatusModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    server_id: str
    ip: str
    online: bool
    checked_at: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {str: lambda v: str(v)}
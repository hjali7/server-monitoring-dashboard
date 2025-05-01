from pydantic import BaseModel, Field
from typing import Optional

class ServerModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    ip: str
    description: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            # برای نمایش درست ObjectId در خروجی
            str: lambda v: str(v)
        }
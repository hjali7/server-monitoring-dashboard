from typing import List, Optional
from pydantic import BaseModel, Field

class ServerModel(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    ip: str
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
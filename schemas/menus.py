# schemas/menu.py
from pydantic import BaseModel
from typing import Optional

class MenuResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    status: Optional[str]
    page_path: Optional[str]

    class Config:
        orm_mode = True


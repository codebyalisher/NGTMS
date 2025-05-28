from pydantic import BaseModel
from typing import Optional
from schemas.menus import MenuResponse

class RolesMenuResponse(BaseModel):
    id: int
    role_id: int
    menu_id: int
    status: Optional[str]
    menu: Optional[MenuResponse]

    class Config:
        orm_mode = True


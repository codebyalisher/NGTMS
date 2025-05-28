# schemas/user.py

from pydantic import BaseModel
from typing import Optional

class RoleResponse(BaseModel):
    id: int
    name: str
    status: Optional[str]

    class Config:
        orm_mode=True
class DepartmentBase(BaseModel):
    id: int
    name: str
    status: Optional[str] = None

    class Config:
        orm_mode = True

class UserLoginResponse(BaseModel):
    id: int
    name: str
    email: str
    picture: Optional[str]
    role: Optional[RoleResponse]
    department: Optional[DepartmentBase]

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    picture: Optional[str]
    role_id: int | None

    class Config:
        from_attributes = True
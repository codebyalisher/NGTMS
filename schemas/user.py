from pydantic import BaseModel

class RoleResponse(BaseModel):
    id: int
    name: str
    status:str

    class Config:
        orm_mode = True

class DepartmentBase(BaseModel):
    id: int
    name: str
    status: str | None = None

    class Config:
        orm_mode = True

class UserLoginResponse(BaseModel):
    id: int
    name: str
    email: str
    picture: str | None = None
    role: RoleResponse
    department: DepartmentBase | None = None

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: str
    password: str


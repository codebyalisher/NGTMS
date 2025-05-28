from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.user import *  # import User here
from models.rolesmenu import *
# models/role.py
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)

    users = relationship("User", back_populates="role")
    roles_menus = relationship("RolesMenu", back_populates="role")

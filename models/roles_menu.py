# models/rolesmenu.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.role import *
from models.menus import *

class RolesMenu(Base):
    __tablename__ = "roles_menus"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("meneuses.id"), nullable=False)
    status = Column(String(50), nullable=True)

    role = relationship("Role", back_populates="roles_menus")
    menu = relationship("Meneus", back_populates="roles_menus")


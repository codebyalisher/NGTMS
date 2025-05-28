from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.role import *
from models.user import *

class RolesMenu(Base):
    __tablename__ = "roles_menus"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("meneus.id"), nullable=False)
    status = Column(String(50), nullable=True)

    role = relationship("User", backref="roles_menus")
    menu = relationship("Meneus", backref="roles_menus")


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Meneus(Base):
    __tablename__ = "meneus"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey("meneus.id"), nullable=True)
    status = Column(String(50), nullable=True)
    page_path = Column(String(255), nullable=True)
    encryption_salt = Column(String(36), nullable=False, default=lambda: str(uuid.uuid4()))

    parent = relationship("Meneus", remote_side=[id], back_populates="children")
    children = relationship("Meneus", back_populates="parent")
    roles_menus = relationship("RolesMenu", back_populates="menu")

from sqlalchemy import Column, BigInteger, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Meneus(Base):
    __tablename__ = "meneuses"  # Matches your actual DB table

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(BigInteger, ForeignKey("meneuses.id"), nullable=True, index=True)
    status = Column(String(50), nullable=False, default="1")
    created_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    page_path = Column(Text, nullable=True)
    encryption_salt = Column(String(36), nullable=False, index=True, default=lambda: str(uuid.uuid4()))

    parent = relationship("Meneus", remote_side=[id], back_populates="children")
    children = relationship("Meneus", back_populates="parent")

    roles_menus = relationship("RolesMenu", back_populates="menu")


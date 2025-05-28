from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from models import *

class SlaConfiguration(Base):
    __tablename__ = "sla_configurations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    response_time = Column(String(100), nullable=True)
    resolution_time = Column(String(100), nullable=True)
    escalated_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    purpose_id = Column(Integer, ForeignKey("purposes.id"), nullable=True)
    is_default = Column(Boolean, default=False)

    department = relationship("Department", back_populates="sla_configuration")
    escalated = relationship("User", back_populates="sla_configurations", foreign_keys=[escalated_to_user_id])


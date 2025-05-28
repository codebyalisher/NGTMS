from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship
from models.user import *
from models.slaconfiguration import SlaConfiguration


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)

    users = relationship("User", back_populates="department")
    sla_configuration = relationship("SlaConfiguration", back_populates="department", uselist=False)
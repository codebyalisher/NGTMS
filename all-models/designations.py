from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Designation(Base):
    __tablename__ = "designations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)

    contacts = relationship("Contact", back_populates="designation")

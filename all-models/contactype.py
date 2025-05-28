from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class ContactType(Base):
    __tablename__ = "contact_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)

    contact_companies = relationship("ContactCompany", back_populates="contact_type")
    contacts = relationship("Contact", back_populates="contact_type")

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.contactype import *

class ContactCompany(Base):
    __tablename__ = "contact_companies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_comp_id = Column(Integer, ForeignKey("contact_companies.id"), nullable=True)
    is_group = Column(Boolean, default=False)
    status = Column(String(50), nullable=True)
    company_code = Column(String(50), nullable=True)
    company_type_id = Column(Integer, ForeignKey("contact_types.id"), nullable=True)

    parent_company = relationship("ContactCompany", remote_side=[id], back_populates="child_companies")
    child_companies = relationship("ContactCompany", back_populates="parent_company")

    contact_type = relationship("ContactType", back_populates="contact_companies")

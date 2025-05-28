from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models import *

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    parent_comp_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    is_group = Column(Boolean, default=False)
    company_code = Column(String(50), nullable=True)
    company_type_id = Column(Integer, ForeignKey("company_types.id"), nullable=True)
    status = Column(String(50), nullable=True)

    parent_company = relationship("Company", remote_side=[id], back_populates="child_companies")
    child_companies = relationship("Company", back_populates="parent_company")
    company_type = relationship("CompanyType", back_populates="companies")
    #projects=relationship("Project",back_populates="company")

    users = relationship("User", back_populates="company")
    tickets = relationship("Tickets", back_populates="company") 

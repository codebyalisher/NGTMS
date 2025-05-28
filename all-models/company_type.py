from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class CompanyType(Base):
    __tablename__ = "company_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)

    companies = relationship("models.company.Company", back_populates="company_type")

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=True)
    project_type_id = Column(Integer, ForeignKey("project_types.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    project_owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    project_type = relationship("ProjectTypes", back_populates="projects")
    company = relationship("Company", back_populates="projects")
    project_owner = relationship("User", back_populates="owned_projects")

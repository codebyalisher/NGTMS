from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class ProjectTypes(Base):
    __tablename__ = "project_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)

    projects = relationship("Project", back_populates="project_type")

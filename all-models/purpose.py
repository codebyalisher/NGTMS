from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, Session
from database import Base

class Purpose(Base):
    __tablename__ = "purposes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("purposes.id"), nullable=True)
    sla_id = Column(Integer, ForeignKey("sla_configurations.id"), nullable=True)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)

    parent = relationship("Purpose", remote_side=[id], back_populates="children")
    children = relationship("Purpose", back_populates="parent", cascade="all, delete-orphan")    
    sla = relationship("SlaConfiguration", back_populates="purposes")
    agent_purpose_links = relationship("AgentPurpose", back_populates="purpose")
    users = relationship(
        "User",
        secondary="agent_purposes",
        back_populates="purposes"
    )


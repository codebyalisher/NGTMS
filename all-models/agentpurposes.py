from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class AgentPurpose(Base):
    __tablename__ = "agent_purposes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    purpose_id = Column(Integer, ForeignKey("purposes.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="agent_purpose_links")
    purpose = relationship("Purpose", back_populates="agent_purpose_links")

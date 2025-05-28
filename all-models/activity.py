from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB  # Only works if using PostgreSQL
from database import Base
from .tickets import Tickets  

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    logs = Column(JSONB, nullable=True)  # fallback to JSON if not PostgreSQL
    ip_address = Column(String(45), nullable=True)  # IPv6-compatible

    tickets = relationship("Tickets", back_populates="activity_logs")

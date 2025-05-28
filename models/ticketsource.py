from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from database import Base  # your Base from SQLAlchemy setup

class TicketSource(Base):
    __tablename__ = "ticket_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
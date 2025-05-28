from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship, Session
from database import Base  # Your declarative base

class TicketStatus(Base):
    __tablename__ = "ticket_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

    # Relationship to Tickets model (one-to-many)
    tickets = relationship("Tickets", back_populates="ticket_status")

    @classmethod
    def get_default(cls, db: Session):
        return db.query(cls).filter(cls.is_default == True).first()

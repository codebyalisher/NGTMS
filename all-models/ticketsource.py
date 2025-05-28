from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from database import Base  # your Base from SQLAlchemy setup

class TicketSource(Base):
    __tablename__ = "ticket_source"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    status = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)

    @classmethod
    def get_default(cls, db: Session):
        return db.query(cls).filter(cls.is_default == True).first()

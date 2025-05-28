from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class StatusWorkflow(Base):
    __tablename__ = "status_workflows"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    from_status_id = Column(Integer, ForeignKey("ticket_status.id"), nullable=False)
    to_status_id = Column(Integer, ForeignKey("ticket_status.id"), nullable=False)
    is_default = Column(Boolean, default=False)

    from_status = relationship("TicketStatus", foreign_keys=[from_status_id])
    to_status = relationship("TicketStatus", foreign_keys=[to_status_id])

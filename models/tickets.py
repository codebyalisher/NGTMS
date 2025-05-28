from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from models import *
# from models.ticketstatus import TicketStatus
# from models.priority import Priority 
# from models.user import User
# from models.slaconfiguration import SlaConfiguration
# from models.ticketsource import TicketSource
# from models.contact import Contact
# from models.ticketattachment import TicketAttachment


class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    ticket_status_id = Column(Integer, ForeignKey("ticket_statuses.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ticket_source_id = Column(Integer, ForeignKey("ticket_sources.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    contact_ref_no = Column(String, nullable=True)
    purpose_type_id = Column(JSONB, nullable=True)
    SLA = Column(Integer, ForeignKey("sla_configurations.id"), nullable=True)
    notification_type_id = Column(JSONB, nullable=True)
    attachments = Column(String, nullable=True) 
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    reminder_flag = Column(Boolean, default=False)
    reminder_datetime = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    internal_note = Column(Text, nullable=True)
    external_note = Column(Text, nullable=True)
    response_time = Column(String, nullable=True)
    resolution_time = Column(String, nullable=True)
    response_time_id = Column(Integer, ForeignKey("sla_configurations.id"), nullable=True)
    resolution_time_id = Column(Integer, ForeignKey("sla_configurations.id"), nullable=True)
    priority_id = Column(Integer, ForeignKey("priorities.id"), nullable=True)
    message = Column(Text, nullable=True)
    requested_email = Column(String, nullable=True)
    to_recipients = Column(JSONB, nullable=True)
    cc_recipients = Column(JSONB, nullable=True)

    # Relationships
    ticket_statuses = relationship("TicketStatus", back_populates="tickets")
    createdBy = relationship("User", foreign_keys=[created_by_id])
    assignedTo = relationship("User", foreign_keys=[assigned_to_id])
    priorities = relationship("Priority", back_populates="tickets")
    attachments = relationship("TicketAttachment", back_populates="ticket")
    company = relationship("Company", back_populates="tickets")
    


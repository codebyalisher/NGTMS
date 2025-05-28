from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB  # Use JSON for SQLite/MySQL
import uuid
from database import Base
from .ticketjourney import TicketJourney


class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    title = Column(String, nullable=False)
    ticket_status_id = Column(Integer, ForeignKey("ticket_status.id"), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    ticket_source_id = Column(Integer, ForeignKey("ticket_source.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    contact_ref_no = Column(String, nullable=True)
    purpose_type_id = Column(JSONB, nullable=True)
    SLA = Column(Integer, ForeignKey("sla_configurations.id"), nullable=True)
    resolution_time_id = Column(Integer, ForeignKey("sla_configurations.id"), nullable=True)
    response_time_id = Column(Integer, ForeignKey("sla_configurations.id"), nullable=True)
    response_time = Column(String, nullable=True)
    resolution_time = Column(String, nullable=True)
    notification_type_id = Column(JSONB, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    reminder_flag = Column(Boolean, nullable=True)
    reminder_datetime = Column(DateTime, nullable=True)
    internal_note = Column(Text, nullable=True)
    external_note = Column(Text, nullable=True)
    priority_id = Column(Integer, ForeignKey("priorities.id"), nullable=True)
    message = Column(Text, nullable=True)
    requested_email = Column(String, nullable=True)
    to_recipients = Column(JSONB, nullable=True)
    cc_recipients = Column(JSONB, nullable=True)
    ticket_id = Column(String, unique=True, index=True)
    is_read = Column(Boolean, default=False)
    comment_id=Column(Integer,ForeignKey("comments.id"))

    # === Relationships ===
    ticketStatus = relationship("TicketStatus", back_populates="tickets")
    createdBy = relationship("User", foreign_keys=[created_by_id], back_populates="created_tickets")
    assignedTo = relationship("User", foreign_keys=[assigned_to_id], back_populates="assigned_tickets")
    ticketSource = relationship("TicketSource", backref="tickets")
    contacts = relationship("Contact", backref="tickets")
    slaConfiguration = relationship("SlaConfiguration", foreign_keys=[SLA], backref="sla_tickets")
    responseTime = relationship("SlaConfiguration", foreign_keys=[response_time_id], backref="response_time_tickets")
    resolutionTime = relationship("SlaConfiguration", foreign_keys=[resolution_time_id], backref="resolution_time_tickets")
    company = relationship("Company", backref="tickets")
    priorities = relationship("Priority", back_populates="tickets")
    replies = relationship("TicketReplies", back_populates="tickets", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="tickets", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="ticket", foreign_keys="[Comment.ticket_id]")

    # === Custom field for assigned user (duplicate relationship)
    assignedUser = relationship("User", foreign_keys=[assigned_to_id], viewonly=True)

    def generate_ticket_id(self, session):
        while True:
            candidate = f"TCKT-{uuid.uuid4().hex[:8].upper()}"
            if not session.query(Tickets).filter_by(ticket_id=candidate).first():
                return candidate

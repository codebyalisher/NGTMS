from sqlalchemy import (
    Column, Integer, String, Text, Boolean, ForeignKey, ARRAY
)
from sqlalchemy.orm import relationship
from database import Base  # assuming you have a Base from your SQLAlchemy setup


class TicketReplies(Base):
    __tablename__ = "ticket_replies"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    replied_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(255), nullable=True)
    message = Column(Text, nullable=True)
    priority_type_id = Column(Integer, ForeignKey("priority.id"), nullable=True)
    reply_type = Column(Integer, ForeignKey("ticket_source.id"), nullable=True)
    attachment_path = Column(String(255), nullable=True)
    internal_notes = Column(Text, nullable=True)
    external_notes = Column(Text, nullable=True)
    is_desc_send_to_contact = Column(Boolean, default=False)
    status_after_reply = Column(Integer, ForeignKey("ticket_status.id"), nullable=True)
    contact_id = Column(Integer, nullable=True)
    contact_ref_no = Column(String(100), nullable=True)
    contact_email = Column(String(255), nullable=True)
    to_recipients = Column(ARRAY(String), nullable=True)
    cc_recipients = Column(ARRAY(String), nullable=True)
    is_reply_from_contact = Column(Boolean, default=False)
    is_contact_notify = Column(Boolean, default=False)
    activity_log = Column(Text, nullable=True)
    is_read = Column(Boolean, default=False)

    # Relationships
    tickets = relationship("Tickets", back_populates="ticket_replies")
    user = relationship("User", back_populates="ticket_replies")
    priority = relationship("Priority")
    reply_type_rel = relationship("TicketSource")
    ticket_status = relationship("TicketStatus")


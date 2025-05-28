from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ContactsPreferences(Base):
    __tablename__ = "contacts_preferences"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    whatsapp_pref = Column(String(100), nullable=True)
    mailing_address_pref = Column(String(255), nullable=True)
    language_pref = Column(String(50), nullable=True)
    email_opt_in = Column(Boolean, default=False)
    whatsapp_opt_in = Column(Boolean, default=False)

    contact = relationship("Contact", back_populates="preferences")

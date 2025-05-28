from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ContactsPhoneNumber(Base):
    __tablename__ = "contacts_phone_numbers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    phone_type = Column(String(50), nullable=True)
    phone_number = Column(String(50), nullable=False)
    is_whatsapp = Column(Boolean, default=False)
    is_preferred = Column(Boolean, default=False)

    contact = relationship(
    "Contact",
    back_populates="phone_numbers",
    foreign_keys="[ContactsPhoneNumber.contact_id]"
)


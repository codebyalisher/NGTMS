from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ContactsSocialLink(Base):
    __tablename__ = "contacts_social_links"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    platform = Column(String(100), nullable=False)
    handle = Column(String(255), nullable=False)

    contact = relationship("Contact", back_populates="social_links")

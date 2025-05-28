from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from .contactphonenumbers import ContactsPhoneNumber
from .contactprefrences import ContactsPreferences
from .contactsociallinks import ContactsSocialLink
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    status = Column(String(50), nullable=True)
    contact_type_id = Column(Integer, ForeignKey("contact_types.id"), nullable=True)
    designation_id = Column(Integer, ForeignKey("designations.id"), nullable=True)
    preferred_contact_method = Column(String(50), nullable=True)
    contact_priority = Column(String(50), nullable=True)
    time_zone = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    picture_url = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    contact_segmentation_id = Column(Integer, ForeignKey("contact_segmentations.id"), nullable=True)

    # Relationships
    contact_type = relationship("ContactType", back_populates="contacts")
    designation = relationship("Designation", back_populates="contacts")
    contact_segmentation = relationship("ContactSegmentation", back_populates="contacts")

    phone_numbers = relationship(
        "ContactsPhoneNumber",
        back_populates="contact",
        foreign_keys=[ContactsPhoneNumber.contact_id]
    )

    preferences = relationship(
        "ContactsPreferences",
        back_populates="contact",
        foreign_keys=[ContactsPreferences.contact_id]
    )

    social_links = relationship(
        "ContactsSocialLink",
        back_populates="contact",
        foreign_keys=[ContactsSocialLink.contact_id]
    )


from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class ContactSegmentation(Base):
    __tablename__ = "contact_segmentations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    is_default = Column(Boolean, default=False)
    status = Column(String(50), nullable=True)

    contacts = relationship("Contact", back_populates="contact_segmentation")

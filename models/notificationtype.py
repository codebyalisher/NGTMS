from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from database import Base

class NotificationType(Base):
    __tablename__ = "notification_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
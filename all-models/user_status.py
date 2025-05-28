from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class UserStatus(Base):
    __tablename__ = "user_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)

    # Reverse relationship
    users = relationship("User", back_populates="status")

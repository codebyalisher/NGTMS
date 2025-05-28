from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_type = Column(String(50), nullable=True)
    comment = Column(String, nullable=False)

    # Explicitly specify foreign keys
    ticket = relationship("Tickets", back_populates="comments", foreign_keys=[ticket_id])
    task = relationship("Tasks", back_populates="comments", foreign_keys=[task_id])
    user = relationship("User", back_populates="comments", foreign_keys=[user_id])

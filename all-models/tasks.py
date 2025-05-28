from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)

    project = relationship("Project", foreign_keys=[project_id])
    ticket = relationship("Tickets", foreign_keys=[ticket_id])
    assigned_user = relationship("User", foreign_keys=[assigned_to])
    comments = relationship("Comment", back_populates="task", foreign_keys="[Comment.task_id]")

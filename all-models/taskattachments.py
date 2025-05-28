from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class TaskAttachments(Base):
    __tablename__ = "task_attachments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    task = relationship("Tasks", foreign_keys=[task_id])
    uploaded_by_user = relationship("User", foreign_keys=[uploaded_by])

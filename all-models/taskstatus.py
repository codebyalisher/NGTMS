from sqlalchemy import Column, Integer, String
from database import Base

class TaskStatus(Base):
    __tablename__ = "task_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    status = Column(String(255), nullable=True)

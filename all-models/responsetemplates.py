from sqlalchemy import Column, Integer, String
from database import Base

class ResponseTemplates(Base):
    __tablename__ = "response_templates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    message = Column(String, nullable=False)

from sqlalchemy import Column, Integer, String
from database import Base

class FieldVariable(Base):
    __tablename__ = "field_variables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    value = Column(String(255), nullable=True)

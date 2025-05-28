from sqlalchemy import Column, Integer, String, Time
from database import Base

class ShiftTypes(Base):
    __tablename__ = "shift_types"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=True)
    from_time = Column(Time, nullable=True)
    to_time = Column(Time, nullable=True)

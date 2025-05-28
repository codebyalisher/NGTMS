from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class TimesheetStatus(Base):
    __tablename__ = 'timesheet_statuses'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=True)

    # Optional: relationship back to Timesheet
    timesheets = relationship('Timesheet', back_populates='ts_status')

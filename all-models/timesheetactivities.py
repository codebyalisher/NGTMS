from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class TimesheetActivities(Base):
    __tablename__ = 'timesheet_activities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=True)

    # Relationship back to Timesheet
    timesheets = relationship('Timesheet', back_populates='timesheet_activity')

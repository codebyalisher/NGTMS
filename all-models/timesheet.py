from sqlalchemy import (
    Column, Integer, String, ForeignKey, Time
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.event import listens_for
from datetime import datetime, timedelta

Base = declarative_base()

class Timesheet(Base):
    __tablename__ = 'timesheets'

    id = Column(Integer, primary_key=True, index=True)
    ts_activity_id = Column(Integer, ForeignKey('timesheet_activities.id'))
    activity_description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    shift_type_id = Column(Integer, ForeignKey('shift_types.id'))
    ts_status_id = Column(Integer, ForeignKey('timesheet_status.id'))
    approved_by_id = Column(Integer, ForeignKey('users.id'))
    approved_date = Column(String, nullable=True)  # or DateTime if you want to store as datetime
    from_time = Column(Time, nullable=True)
    to_time = Column(Time, nullable=True)
    total_time_consumed = Column(String(5), nullable=True)  # Format HH:mm

    # Relationships
    timesheet_activity = relationship('TimesheetActivities', back_populates='timesheets')
    user = relationship('User', foreign_keys=[user_id])
    project = relationship('Project')
    shift_type = relationship('ShiftTypes')
    ts_status = relationship('TimesheetStatus')
    approved_by = relationship('User', foreign_keys=[approved_by_id])

# Event listener to calculate total_time_consumed on insert/update
@listens_for(Timesheet, "before_insert")
@listens_for(Timesheet, "before_update")
def calculate_total_time(mapper, connection, target):
    if target.from_time and target.to_time:
        start = datetime.combine(datetime.today(), target.from_time)
        end = datetime.combine(datetime.today(), target.to_time)

        # Handle overnight shift (to_time < from_time)
        if end < start:
            end += timedelta(days=1)

        diff = end - start
        hours, remainder = divmod(diff.seconds, 3600)
        minutes = remainder // 60
        target.total_time_consumed = f"{hours:02d}:{minutes:02d}"

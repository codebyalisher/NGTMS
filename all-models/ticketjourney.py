from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Session, declarative_base
from datetime import datetime

Base = declarative_base()

class TicketJourney(Base):
    __tablename__ = 'ticket_journeys'

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=False)
    from_agent = Column(Integer, ForeignKey('users.id'), nullable=True)
    to_agent = Column(Integer, ForeignKey('users.id'), nullable=True)
    from_status = Column(Integer, ForeignKey('ticket_status.id'), nullable=True)
    to_status = Column(Integer, ForeignKey('ticket_status.id'), nullable=True)
    actioned_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    logged_time = Column(DateTime, default=datetime.utcnow)
    total_time_diff = Column(Integer, default=0)  # Stored in seconds

    ticket = relationship('Tickets', back_populates='journeys')
    from_agent_rel = relationship('User', foreign_keys=[from_agent])
    to_agent_rel = relationship('User', foreign_keys=[to_agent])
    from_status_rel = relationship('TicketStatus', foreign_keys=[from_status])
    to_status_rel = relationship('TicketStatus', foreign_keys=[to_status])
    actioned_by_rel = relationship('User', foreign_keys=[actioned_by])

    @staticmethod
    def create_with_time_diff(session: Session, **kwargs):
        """
        Create a new TicketJourney record and calculate total_time_diff 
        compared to the last journey for the same ticket.
        """
        ticket_id = kwargs.get('ticket_id')
        logged_time = kwargs.get('logged_time', datetime.utcnow())

        last_journey = (
            session.query(TicketJourney)
            .filter(TicketJourney.ticket_id == ticket_id)
            .order_by(TicketJourney.logged_time.desc())
            .first()
        )

        if last_journey:
            prev_time = last_journey.logged_time
            time_diff = int((logged_time - prev_time).total_seconds())
        else:
            time_diff = 0

        kwargs['total_time_diff'] = time_diff
        kwargs['logged_time'] = logged_time

        journey = TicketJourney(**kwargs)
        session.add(journey)
        session.commit()
        session.refresh(journey)
        return journey

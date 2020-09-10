from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Events(Base):
    __tablename__ = "mvd_event"

    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String)
    event_description = Column(String)
    linked_msisdn = Column(String)
    target_amount = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String, default='open')
    contribution_limit_type = Column(String)
    contribution_limit_amount = Column(String)
    total_contribution = Column(Integer)


class Participants(Base):
    __tablename__ = "mvd_event_participants"

    record_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer)
    # event_id = Column(Integer, ForeignKey("events.event_id"))
    member_id = Column(Integer)
    linked_msisdn = Column(String)
    amount_contributed = Column(Integer, default=0)
    amount_due = Column(Integer)
    status = Column(String, default='not_paid')
    last_updated = Column(Date)

    # event = relationship("Event", back_populates="items")


class EventBook(Base):
    __tablename__ = "mvd_events_book"

    event_book_id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer)
    trans_date = Column(Date)
    transaction_id = Column(Integer, default=0)
    transaction_amount = Column(Integer)
    transaction_type = Column(String)
    member_id = Column(Integer)
    linked_msisdn = Column(String)
    comment = Column(String, nullable=True)
    anonymous = Column(String, default="No")

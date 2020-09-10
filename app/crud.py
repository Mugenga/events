from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now

from . import models, schemas
import logging


def handle_create_event(db: Session, event: schemas.EventCreate):
    event = models.Events(
        event_name=event.event_name,
        event_description=event.event_description,
        linked_msisdn=event.linked_msisdn,
        target_amount=event.target_amount,
        start_date=event.start_date,
        end_date=event.end_date,
        contribution_limit_type=event.contribution_limit_type,
        contribution_limit_amount=event.contribution_limit_amount,
        total_contribution=0
    )
    db.add(event)
    failed = False

    try:
        db.commit()
        db.refresh(event)
    except Exception as e:
        # log your exception in the way you want -> log to file, log as error with default logging, send by email.
        # It's upon you
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        db.rollback()
        db.flush()  # for resetting non-commited .add()
        failed = True

    if failed:
        return dict(response_code=100, response_message="Could not create event")
    else:
        return dict(response_code=100, response_message="Event Created Successfully", event=event)


def get_all_events(db: Session):
    events = db.query(models.Events).all()
    return dict(response_code=100, events=events)


def get_user_events(db: Session, msisdn: str):
    events = db.query(models.Events).filter(models.Events.linked_msisdn == msisdn).all()
    return dict(response_code=100, events=events)


def handle_edit_event(db: Session, event_id: int, event: schemas.EventEdit):
    event = db.query(models.Events).filter_by(models.Events.event_id == event_id) \
        .update(event)
    db.commit()
    db.refresh(event)

    return dict(response_code=100, response_message="successful", event=event)


def handle_adding_member(db: Session, participant: schemas.ParticipantCreate):
    participant = models.Participants(
        event_id=participant.event_id,
        member_id=participant.member_id,
        linked_msisdn=participant.linked_msisdn,
        amount_due=participant.amount_due,
        last_updated=now()
    )
    db.add(participant)
    failed = False
    try:
        db.commit()
        db.refresh(participant)
    except Exception as e:
        # log your exception in the way you want -> log to file, log as error with default logging, send by email.
        # It's upon you
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        db.rollback()
        db.flush()  # for resetting non-commited .add()
        failed = True

    if failed:
        return dict(response_code=101, response_message="Could not Add Member")
    else:
        return dict(response_code=100, response_message="Member Added Successfully")


def handle_remove_member(db: Session, data: schemas.ParticipantBase):
    member = db.query(models.Participants) \
        .filter(models.Participants.event_id == data.event_id, models.Participants.member_id == data.member_id) \
        .delete()

    failed = False
    try:
        db.commit()
    except Exception as e:
        # log your exception in the way you want -> log to file, log as error with default logging, send by email.
        # It's upon you
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        db.rollback()
        db.flush()  # for resetting non-commited .add()
        failed = True

    if failed:
        return dict(response_code=101, response_message="Could not Remove Member")
    else:
        return dict(response_code=100, response_message="Member Removed Successfully")


def get_event_members(db: Session, event_id: int):
    members = db.query(models.Participants).filter(models.Participants.event_id == event_id).all()
    return dict(response_code=100, members=members)


def get_event(db: Session, event_id: int):
    event = db.query(models.Events).filter(models.Events.event_id == event_id).first()
    return event


def handle_contribution(db: Session, contribution: schemas.EventBookCreate):
    contribution = models.EventBook(
        event_id=contribution.event_id,
        trans_date=now(),
        transaction_id=contribution.transaction_id,
        transaction_amount=contribution.transaction_amount,
        transaction_type=contribution.transaction_type,
        member_id=contribution.member_id,
        linked_msisdn=contribution.linked_msisdn,
        comment=contribution.comment,
        anonymous=contribution.anonymous,
    )
    db.add(contribution)
    failed = False

    try:
        db.commit()
        db.refresh(contribution)
    except Exception as e:
        # log your exception in the way you want -> log to file, log as error with default logging, send by email.
        # It's upon you
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        db.rollback()
        db.flush()  # for resetting non-commited .add()
        failed = True

    if failed:
        return dict(response_code=100, response_message="Could not Contribute")
    else:
        return dict(response_code=100, response_message="Contribution Made Successfully")


def handle_withdrawal(db: Session, withdraw: schemas.EventBookCreate):
    withdraw = models.EventBook(
        event_id=withdraw.event_id,
        trans_date=now(),
        transaction_id=withdraw.transaction_id,
        transaction_amount=withdraw.transaction_amount,
        transaction_type=withdraw.transaction_type,
        member_id=withdraw.member_id,
        linked_msisdn=withdraw.linked_msisdn,
        comment=withdraw.comment,
        anonymous=withdraw.anonymous,
    )
    db.add(withdraw)
    failed = False

    try:
        db.commit()
        db.refresh(withdraw)
    except Exception as e:
        # log your exception in the way you want -> log to file, log as error with default logging, send by email.
        # It's upon you
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        db.rollback()
        db.flush()  # for resetting non-commited .add()
        failed = True

    if failed:
        return dict(response_code=100, response_message="Could not Withdraw")
    else:
        return dict(response_code=100, response_message="Withdrawal Made Successfully")

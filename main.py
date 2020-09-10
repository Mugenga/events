from typing import List

from sqlalchemy.orm import Session

from app import crud, schemas

from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel

from app.database import SessionLocal

app = FastAPI(debug=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Event(BaseModel):
    id: int


class Contribute(BaseModel):
    amount: int


class Withdraw(BaseModel):
    amount: int


@app.post("/events/create")
def add_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.handle_create_event(db=db, event=event)


@app.get("/events")
def view_events(db: Session = Depends(get_db)):
    return crud.get_all_events(db=db)


@app.get("/events/viewbyme/{msisdn}")
def view_user_events(msisdn: str, db: Session = Depends(get_db)):
    return crud.get_user_events(db=db, msisdn=msisdn)


@app.post("/events/edit/{event_id}")
def edit_event(event: schemas.EventEdit, event_id: int, db: Session = Depends(get_db)):
    return crud.handle_edit_event(db=db, event_id=event_id, event=event)


@app.post("/members/add")
def add_member(participant: schemas.ParticipantCreate, db: Session = Depends(get_db)):
    return crud.handle_adding_member(db=db, participant=participant)


@app.post("/members/remove")
def remove_member(data: schemas.ParticipantBase, db: Session = Depends(get_db)):
    return crud.handle_remove_member(db=db, data=data)


@app.get("/members/view/{event_id}")
def view_event_members(event_id: int, db: Session = Depends(get_db)):
    return crud.get_event_members(db=db, event_id=event_id)


@app.get("/events/view/{event_id}", response_model=schemas.EventCreate)
def view_event(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event(db=db, event_id=event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event Not Found")
    return event


@app.post("/contribute")
def contribute(contribution: schemas.EventBookCreate, db: Session = Depends(get_db)):
    return crud.handle_contribution(db=db, contribution=contribution)


@app.post("/withdraw")
def withdraw(withdraw: schemas.EventBookCreate, db: Session = Depends(get_db)):
    return crud.handle_withdrawal(db=db, withdraw=withdraw)

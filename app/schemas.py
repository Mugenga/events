from typing import List

from mysql.connector import Date
from pydantic import BaseModel
from typing import Optional


class EventBase(BaseModel):
    event_name: str

    class Config:
        orm_mode = True


class EventCreate(EventBase):
    event_description: Optional[str] = None
    linked_msisdn: Optional[str]
    target_amount: Optional[str]
    start_date: Optional[Date]
    end_date: Optional[Date]
    contribution_limit_type: Optional[str]
    contribution_limit_amount: Optional[str]


class EventEdit(EventBase):
    event_description: str
    linked_msisdn: str
    target_amount: str
    start_date: str
    end_date: str
    contribution_limit_type: str
    contribution_limit_amount: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class ParticipantBase(BaseModel):
    event_id: int
    member_id: int


class ParticipantCreate(ParticipantBase):
    linked_msisdn: Optional[str]
    amount_due: Optional[str]


class EventBookBase(BaseModel):
    event_id: int


class EventBookCreate(EventBookBase):
    transaction_id: int
    transaction_amount: int
    transaction_type: str
    member_id: int
    linked_msisdn: int
    comment: str
    anonymous: str



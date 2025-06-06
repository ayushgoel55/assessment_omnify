import uuid

from enum import Enum
from pydantic import BaseModel, EmailStr,Field
from datetime import datetime


class Status(Enum):
    active = 1
    in_active = -1

class ModificationOperation(Enum):
    add = 1
    update = 2
    delete = 3



class ClassOfferedRequest(BaseModel):
    class_name: str
    start_time: datetime|None = None
    end_time:datetime|None = None
    capacity: int = 0
    batch_creation: datetime|None = None
    status: Status
    modified_by: str
    instructor:str


class UserEnrolledClassesRequest(BaseModel):
    user_id: uuid.UUID
    class_id: uuid.UUID
    subscription_status: int
    modified_by: str
    created_at: datetime|None = None



class UserRequest(BaseModel):
    user_name: str
    email: EmailStr

    modified_by: str


class ClassRequest(BaseModel):
        class_name:str
        instructor:str
        start_time:datetime
        end_time:datetime
        capacity:int
        batch_creation:datetime=datetime.now()
        status:Status
        modified_by:str

class SubscriptionStatus(Enum):
    ACTIVE = 1
    INACTIVE = 0

class BookingApi(BaseModel):

    user_name:str|None= Field(None, alias="client_name")
    user_email:str|None= Field(None, alias="client_email")
    class_id: uuid.UUID

class BookingRequest(BookingApi):
    user_id: uuid.UUID | None = None
    modified_by: str


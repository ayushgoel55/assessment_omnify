import uuid
from sqlalchemy import Column, UUID, String, SmallInteger, DateTime, func,Integer
from datetime import datetime

from sqlalchemy.orm import relationship

from src.models.db_connection import Base


class ClassOffered(Base):
    __tablename__="classes_offered"
    class_id=Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4())
    class_name=Column(String,nullable=False)
    start_time=Column(DateTime)
    end_time=Column(DateTime)
    capacity=Column(SmallInteger,default=0)
    batch_creation=Column(DateTime,default=datetime.now())
    status=Column(SmallInteger,nullable=False)
    modified_at = Column(DateTime, default=func.now(), on_update=func.now(), nullable=False)
    modified_by = Column(String, nullable=False)
    modification_operation = Column(String, nullable=False)
    instructor=Column(String,nullable=False)
    left_seats=Column(Integer,default=0)

    user_enrolled=relationship('UserEnrolledClasses',back_populates="class_detail",uselist=True)


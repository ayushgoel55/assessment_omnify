from sqlalchemy import Column, UUID, String, DATETIME,func
from sqlalchemy.orm import relationship

from src.models.db_connection import Base
import uuid


class User(Base):
    __tablename__="user"
    id=Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4())
    user_name=Column(String,nullable=False)
    email=Column(String,nullable=False)

    created_at=Column(DATETIME,default=func.now(),nullable=False)
    modified_at=Column(DATETIME,default=func.now(),on_update=func.now(),nullable=False)
    modified_by=Column(String,nullable=False)
    modification_operation=Column(String,nullable=False)

    enrolled_courses=relationship("UserEnrolledClasses",back_populates="user_detail",uselist=True)



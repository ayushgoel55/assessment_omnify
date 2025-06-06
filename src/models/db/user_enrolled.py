from sqlalchemy import Column, UUID, SmallInteger, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from src.models.db_connection import Base
import uuid


class UserEnrolledClasses(Base):
    __tablename__="user_enrolled_class_association"
    enrollment_id=Column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4())
    user_id=Column(UUID(as_uuid=True),ForeignKey("user.id"),nullable=False)
    class_id=Column(UUID(as_uuid=True),ForeignKey("classes_offered.class_id"),nullable=False)
    subscription_status=Column(SmallInteger,nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    modified_at = Column(DateTime, default=func.now(), on_update=func.now(), nullable=False)
    modified_by = Column(String, nullable=False)
    modification_operation = Column(String, nullable=False)

    user_detail=relationship("User",back_populates="enrolled_courses",uselist=False)
    class_detail=relationship("ClassOffered",back_populates="user_enrolled",uselist=False)
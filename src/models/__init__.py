# Import all models here so SQLAlchemy can find them
from src.models.db.user import User
from src.models.db.classes import ClassOffered
from src.models.db.user_enrolled import UserEnrolledClasses

__all__ = ["User", "ClassOffered", "UserEnrolledClasses"]

import uuid
from typing import Any, Tuple
from fastapi import HTTPException
from src.repository.user_class_enrollment import BookingRepository
from src.repository.class_repository import ClassRepository
from src.repository.user_repository import UserRepository
from src.models.db.classes import ClassOffered
from src.utils.singleton import singleton
from src.validators.base_validator import BaseValidator

@singleton
class BookingValidator(BaseValidator):
    def __init__(
        self,
        booking_repo: BookingRepository,
        class_repo: ClassRepository,
        user_repo: UserRepository
    ):
        print("BookingValidator was initialized")
        self.booking_repo = booking_repo
        self.class_repo = class_repo
        self.user_repo = user_repo

    async def validate(self, inp: Any) -> Tuple[bool, list[Any],uuid.UUID]:
        has_error = False
        error_messages: list[str] = []


        if not (inp.user_id or inp.user_email or inp.user_name):
            has_error = True
            error_messages.append("Provide at least one of user_id, user_email, or user_name.")


        user = await self.user_repo.get_user(user_id=inp.user_id,email=inp.user_email,user_name=inp.user_name)

        user_id = user.id

        #  Check that the class exists
        class_obj= await self.class_repo.get_class(class_id=inp.class_id)
        if not class_obj:
            has_error = True
            error_messages.append("Invalid class ID.")
        else:
            #  If class exists, check capacity
            enrolled_count = await self.booking_repo.count_enrollments(class_id=inp.class_id)
            if enrolled_count >= class_obj.capacity:
                has_error = True
                error_messages.append("No available seats in the class.")

        #  If both user and class exist, check for existing enrollment
        if user_id and class_obj:
            existing_enrollment = await self.booking_repo.get_booking(
                user_id=user_id,
                class_id=inp.class_id
            )
            if existing_enrollment:
                has_error = True
                error_messages.append("User already enrolled in this class.")

        return has_error, error_messages,user_id

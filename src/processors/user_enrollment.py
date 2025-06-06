from typing import Any, Tuple
from fastapi import HTTPException, status

from src.mappers.user_class_enrolled_association import UserEnrolledClassesMapper
from src.processors.base_processor import BaseProcessor
from src.repository.user_class_enrollment import BookingRepository
from src.utils.singleton import singleton
from src.validators.user_course_enrollment import BookingValidator


@singleton
class BookingProcessor(BaseProcessor):
    def __init__(self, booking_mapper: UserEnrolledClassesMapper, booking_repo: BookingRepository, validator: BookingValidator):
        print("BookingProcessor was initiated")
        self.booking_mapper = booking_mapper
        self.booking_repo = booking_repo
        self.validator = validator

    async def process(self, inp: Any) -> Tuple[bool, list[Any]]:
        has_error, error_messages,user_id = await self.validator.validate(inp)
        if has_error:
            return has_error, error_messages
        inp.user_id=user_id

        booking_entity = await self.booking_mapper.map(inp)

        status_code = await self.booking_repo.add_booking(booking_entity)

        if status_code != 200:
            has_error = True
            error_messages.append("Unable to create new booking")

        return has_error, error_messages

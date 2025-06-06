import uuid

from fastapi import APIRouter, HTTPException

from src.models.db_connection import AsyncSessionGenerator
from src.models.request_model.requests import BookingRequest, BookingApi
from src.repository.user_class_enrollment import BookingRepository
from src.repository.class_repository import ClassRepository
from src.repository.user_repository import UserRepository
from src.validators.user_course_enrollment import BookingValidator
from src.mappers.user_class_enrolled_association import UserEnrolledClassesMapper
from src.processors.user_enrollment import BookingProcessor

booking_router = APIRouter(
    tags=['booking']
)

@booking_router.post("/book")
async def create_booking(data: BookingApi):
    session = AsyncSessionGenerator()
    if not data.user_name and not data.user_email:
        raise HTTPException(status_code=400,detail="provide user_id or email")
    payload = data.model_dump()

    payload.update({
        "modified_by": data.user_email,
        "user_id": None
    })
    print(payload, "payload")
    data = BookingRequest(**payload)
    print(data.model_dump(), "data")
    booking_repo = BookingRepository(session=session)
    class_repo = ClassRepository(session=session)
    user_repo = UserRepository(session=session)

    validator = BookingValidator(
        booking_repo=booking_repo,
        class_repo=class_repo,
        user_repo=user_repo
    )

    booking_mapper = UserEnrolledClassesMapper()
    processor = BookingProcessor(
        validator=validator,
        booking_repo=booking_repo,
        booking_mapper=booking_mapper
    )

    has_error, error_messages = await processor.process(inp=data)
    if has_error:
        raise HTTPException(status_code=400, detail=error_messages)

    return "added successfully"



@booking_router.get("/bookings")
async def get_user_enrolled_classes(user_id: uuid.UUID|None=None ,email_id: str|None=None
):
    if not user_id and not email_id:
        raise HTTPException(status_code=400, detail="Provide either user_id or email_id")

    session = AsyncSessionGenerator()
    user_repo = UserRepository(session=session)
    booking_repo = BookingRepository(session=session)

    # Resolve user from ID or name
    user = await user_repo.get_user(email=email_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    classes = await booking_repo.get_enrolled_classes_for_user(user_id=user.id)

    return classes

from fastapi import HTTPException
from sqlalchemy import select, and_, func
from uuid import UUID

from sqlalchemy.orm import selectinload

from src.models.db.classes import ClassOffered
from src.models.db.user import User
from src.models.db.user_enrolled import UserEnrolledClasses
from src.utils.singleton import singleton


@singleton
class BookingRepository:
    def __init__(self, session):
        print("BookingRepository was initiated")
        self.session_generator = session




    async def add_booking(self, entry: UserEnrolledClasses) -> int:
        async for session in self.session_generator.get_session():
            try:
                # Fetch the class and decrement left_seats
                class_obj = await session.get(ClassOffered, entry.class_id)
                if class_obj.left_seats <= 0:
                    raise HTTPException(status_code=400, detail="No available seats left in the class")

                class_obj.left_seats -= 1  # Reduce seat count

                session.add(entry)

                await session.commit()
                return 200
            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f"Error adding booking: {error}")


    async def get_booking(self, user_id: UUID, class_id: UUID) -> UserEnrolledClasses | None:
        async for session in self.session_generator.get_session():
            try:
                result = await session.execute(
                    select(UserEnrolledClasses).where(
                        and_(
                            UserEnrolledClasses.user_id == user_id,
                            UserEnrolledClasses.class_id == class_id
                        )
                    )
                )
                return result.scalars().first()
            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f"Error fetching booking: {error}")


    async def get_enrolled_classes_for_user(self, user_id: UUID | None = None, user_name: str | None = None) -> dict:
        async for session in self.session_generator.get_session():
            try:
                if not user_id and not user_name:
                    raise HTTPException(status_code=400, detail="Provide user_id or user_name")

                # Resolve user
                user_query = select(User)
                if user_id:
                    user_query = user_query.where(User.id == user_id)
                elif user_name:
                    user_query = user_query.where(User.user_name == user_name)

                user_result = await session.execute(user_query)
                user = user_result.scalars().first()

                if not user:
                    raise HTTPException(status_code=404, detail="User not found")

                # Get enrolled classes
                result = await session.execute(
                    select(UserEnrolledClasses)
                    .options(selectinload(UserEnrolledClasses.class_detail))
                    .where(UserEnrolledClasses.user_id == user.id)
                )
                enrollments = result.scalars().all()
                class_details = [e.class_detail for e in enrollments if e.class_detail]

                # Build response structure
                return {
                    "user_id": str(user.id),
                    "user_name": user.user_name,
                    "total_classes": len(class_details),
                    "enrolled_classes": [
                        {
                            "class_id": str(cls.class_id),
                            "class_name": cls.class_name,
                            "start_time": cls.start_time,
                            "end_time": cls.end_time,
                            "capacity": cls.capacity,
                            "status": cls.status
                        }
                        for cls in class_details
                    ]
                }

            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f"Error fetching enrolled classes: {error}")

    async def count_enrollments(self, class_id: UUID) -> int:
        async for session in self.session_generator.get_session():
            try:
                result = await session.execute(
                    select(func.count()).select_from(UserEnrolledClasses).where(UserEnrolledClasses.class_id == class_id)
                )
                return result.scalar() or 0
            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f"Error counting enrollments: {error}")

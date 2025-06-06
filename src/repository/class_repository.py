import uuid

from fastapi import HTTPException
from sqlalchemy import select, and_
from src.models.db.classes import ClassOffered
from src.utils.singleton import singleton

@singleton
class ClassRepository:
    def __init__(self, session):
        print("ClassRepository was initiated")
        self.session_generator = session

    async def add_class(self, entry: ClassOffered) :
        async for session in self.session_generator.get_session():
            try:
                session.add(entry)
                await session.commit()
                return entry.class_id
            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f"Error adding class: {error}")

    async def get_class(self, class_name: str | None = None, class_id: uuid.UUID | None = None):
        async for session in self.session_generator.get_session():
            try:
                condition = []

                if class_name:
                    condition.append(ClassOffered.class_name == class_name)
                if class_id:
                    condition.append(ClassOffered.class_id == class_id)

                # If conditions are provided, filter; otherwise, return all
                if condition:
                    result = await session.execute(select(ClassOffered).where(and_(*condition)))
                    return result.scalars().first()
                else:
                    result = await session.execute(select(ClassOffered))
                    return result.scalars().all()

            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400, detail=f"Error fetching class: {error}")
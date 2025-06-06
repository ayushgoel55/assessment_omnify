from typing import Any, Tuple
from src.repository.class_repository import ClassRepository
from src.utils.singleton import singleton
from src.validators.base_validator import BaseValidator

@singleton
class ClassValidator(BaseValidator):
    def __init__(self, class_repo: ClassRepository):
        print("ClassValidator was initialized")
        self.class_repo = class_repo

    async def validate(self, inp: Any) -> Tuple[bool, list[Any]]:
        has_error = False
        error_messages = []

        if not inp.class_name:
            has_error = True
            error_messages.append("Class name is required")

        if not inp.status:
            has_error = True
            error_messages.append("Status is required")

        if not inp.capacity:
            has_error = True
            error_messages.append("capacity is required")
        elif inp.capacity<=0:
            has_error = True
            error_messages.append("capacity should be more than zero")
        if not inp.start_time and not inp.end_time :
            has_error=True
            error_messages.append("start_time and end_time cant be empty")




        # Optional: Check for duplicate class
        existing = await self.class_repo.get_class(inp.class_name)
        if existing:
            has_error = True
            error_messages.append("A class with this name already exists")

        return has_error, error_messages

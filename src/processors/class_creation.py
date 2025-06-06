import uuid
from typing import Any, Tuple
from fastapi import HTTPException, status

from src.mappers.class_offered import ClassOfferedMapper
from src.processors.base_processor import BaseProcessor
from src.repository.class_repository import ClassRepository
from src.utils.singleton import singleton
from src.validators.class_creation import ClassValidator


@singleton
class ClassCreationProcessor(BaseProcessor):
    def __init__(self, class_mapper:ClassOfferedMapper, class_repo:ClassRepository, validator:ClassValidator):
        print("ClassCreationProcessor was initiated")
        self.class_mapper = class_mapper
        self.class_repo = class_repo
        self.validator = validator

    async def process(self, inp: Any) -> Tuple[bool, list[Any],uuid.UUID|None]:
        has_error, error_messages = await self.validator.validate(inp)
        if has_error:
            return has_error, error_messages,None

        class_entity = await self.class_mapper.map(inp)
        class_id = await self.class_repo.add_class(class_entity)


        return has_error,error_messages,class_id


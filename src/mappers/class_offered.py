import uuid
from typing import Any
from datetime import datetime
from src.mappers.base_mapper import BaseMapper
from src.models.db.classes import ClassOffered
from src.models.request_model.requests import ModificationOperation, ClassRequest, Status
from src.utils.singleton import singleton


@singleton
class ClassOfferedMapper(BaseMapper):
    def __init__(self):
        print("ClassOfferedMapper was initiated")

    async def map(self, inp: ClassRequest) -> ClassOffered:
        mapper_data = ClassOffered()
        mapper_data.class_id = uuid.uuid4()
        mapper_data.class_name = inp.class_name
        mapper_data.start_time = inp.start_time
        mapper_data.instructor=inp.instructor
        mapper_data.end_time = inp.end_time
        mapper_data.capacity = inp.capacity if hasattr(inp, "capacity") else 0
        mapper_data.batch_creation = inp.batch_creation if hasattr(inp, "batch_creation") else datetime.now()
        mapper_data.status = Status.active.value
        mapper_data.modified_at = datetime.now()
        mapper_data.modified_by = inp.modified_by
        mapper_data.modification_operation = ModificationOperation.add.value
        mapper_data.left_seats=inp.capacity

        return mapper_data

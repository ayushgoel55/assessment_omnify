from fastapi import APIRouter, HTTPException

from src.mappers.class_offered import ClassOfferedMapper
from src.models.db_connection import AsyncSessionGenerator
from src.models.request_model.requests import ClassRequest
from src.processors.class_creation import ClassCreationProcessor
from src.repository.class_repository import ClassRepository
from src.validators.class_creation import ClassValidator

class_router=APIRouter(
    tags=['class']
)

@class_router.post("/class")
async def create_booking(data:ClassRequest):
    session=AsyncSessionGenerator()
    class_repo=ClassRepository(session=session)
    validator=ClassValidator(class_repo=class_repo)
    class_mapper=ClassOfferedMapper()
    processor=ClassCreationProcessor(validator=validator,class_repo=class_repo,class_mapper=class_mapper)
    has_error,error_messages,result=await processor.process(inp=data)
    if has_error:
        raise HTTPException(status_code=400,detail=error_messages)
    return  result if result else 400


@class_router.get("/class")
async def create_booking():
    session=AsyncSessionGenerator()
    class_repo=ClassRepository(session=session)
    result=await class_repo.get_class()
    exclude = {
        "modified_at",
        "modified_by",
        "capacity",
        "status",
        "modification_operation",
        "start_time",
        "end_time"
    }

    filtered = []
    for obj in result:
        data = obj.__dict__.copy()
        data.pop("_sa_instance_state", None)
        filtered.append({k: v for k, v in data.items() if k not in exclude})

    return filtered




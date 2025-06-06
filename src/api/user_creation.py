import json
from fastapi import APIRouter,HTTPException


from src.mappers.user import UserMapper
from src.models.db_connection import AsyncSessionGenerator
from src.models.request_model.requests import UserRequest
from src.processors.user_creation import UserCreationProcessor
from src.repository.user_repository import UserRepository
from src.validators.user_creation import UserCreationValidator

user_router=APIRouter(
    tags=["user"]
)

@user_router.post("/user")
async def create_user(data:UserRequest):
    session=AsyncSessionGenerator()
    user_repo=UserRepository(session=session)
    validator=UserCreationValidator(user_repo=user_repo)
    user_mapper=UserMapper()
    processor=UserCreationProcessor(validator=validator,user_repo=user_repo,user_mapper=user_mapper)
    has_error,error_messages=await processor.process(inp=data)
    if has_error:
        raise HTTPException(status_code=400,detail=error_messages)
    return "added successfully"

@user_router.get("/user")
async def fetch_user_detail(email:str|None=None,user_name:str|None=None):
    try:
        if (not email or email in [""," "] ) and not user_name:
            raise HTTPException(status_code=400,detail="provide the argument asked")
        session = AsyncSessionGenerator()
        user_repo = UserRepository(session=session)

        result=await user_repo.get_user(user_name=user_name, email=email)
        # by default result will be empty
        return result
    except Exception as error:
        raise HTTPException(status_code=400,detail=error)
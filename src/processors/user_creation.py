
from typing import Any, Tuple

from starlette import status
from fastapi import HTTPException
from src.mappers.user import UserMapper
from src.models.request_model.requests import UserRequest
from src.processors.base_processor import BaseProcessor
from src.repository.user_repository import UserRepository
from src.utils.singleton import singleton
from src.validators.user_creation import UserCreationValidator


@singleton
class UserCreationProcessor(BaseProcessor):
    def __init__(self,user_mapper:UserMapper,user_repo:UserRepository,validator:UserCreationValidator):
        print("UserCreationProcessor was initiated")
        self.user_repo=user_repo
        self.validator=validator
        self.user_mapper=user_mapper

    async def process(self,inp:UserRequest) ->Tuple[bool,list[Any]]:
        has_error,error_messages=await self.validator.validate(inp)
        if has_error:
            return has_error,error_messages

        user_entity = await self.user_mapper.map(inp=inp)

        # Add to DB
        status_code_ = await self.user_repo.add_user(user_entity)
        if status_code_ == 200:
            return has_error,error_messages
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )



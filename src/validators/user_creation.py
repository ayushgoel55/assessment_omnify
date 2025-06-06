from typing import Any, Tuple

from src.repository.user_repository import UserRepository
from src.utils.singleton import singleton
from src.validators.base_validator import BaseValidator


@singleton
class UserCreationValidator(BaseValidator):
    def __init__(self,user_repo:UserRepository):
        print("UserCreationValidator was initialized")
        self.user_repo=user_repo
    async def validate(self,inp:Any) ->Tuple[bool,list[Any]]:
        has_error=False
        error_messages=[]
        if not inp.email:
            has_error=True
            error_messages.append("email was not provided")

        if inp.email:
            result=await self.user_repo.get_user(email=inp.email)
            if result:
                has_error=True
                error_messages.append("the user with this email already exists")
        return has_error,error_messages


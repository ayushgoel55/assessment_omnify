import uuid
from typing import Any
from datetime import datetime
from src.mappers.base_mapper import BaseMapper
from src.models.db.user import User
from src.models.request_model.requests import ModificationOperation, UserRequest
from src.utils.singleton import singleton


@singleton
class UserMapper(BaseMapper):
    def __init__(self):
        print("UserMapper was initiated")

    async def map(self,inp:UserRequest) ->Any:
        mapper_data=User()
        mapper_data.user_name=inp.user_name
        mapper_data.created_at=datetime.now()
        mapper_data.modified_by=inp.modified_by
        mapper_data.modified_at=datetime.now()
        mapper_data.id=uuid.uuid4()
        mapper_data.email=inp.email
        mapper_data.modification_operation=ModificationOperation.add.value
        return mapper_data


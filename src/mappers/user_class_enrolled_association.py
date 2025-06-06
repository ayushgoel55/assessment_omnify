import uuid
from datetime import datetime

from src.mappers.base_mapper import BaseMapper
from src.models.db.user_enrolled import UserEnrolledClasses

from src.utils.singleton import singleton
from src.models.request_model.requests import ModificationOperation, UserEnrolledClassesRequest, Status

# for linking user to the class
@singleton
class UserEnrolledClassesMapper(BaseMapper):
    def __init__(self):
        print("UserEnrolledClassesMapper was initiated")

    async def map(self, inp: UserEnrolledClassesRequest) -> UserEnrolledClasses:
        mapper_data = UserEnrolledClasses()
        mapper_data.enrollment_id = uuid.uuid4()
        mapper_data.user_id = inp.user_id
        mapper_data.class_id = inp.class_id
        mapper_data.subscription_status = Status.active.value
        mapper_data.created_at = datetime.now()
        mapper_data.modified_at = datetime.now()
        mapper_data.modified_by = inp.modified_by
        mapper_data.modification_operation = ModificationOperation.add.value
        return mapper_data

import uuid

from fastapi import HTTPException

from src.models.db.user import User
from sqlalchemy import  select,and_
from src.models.session_yeild import SessionGenerator
from src.utils.singleton import singleton


@singleton
class UserRepository:
    def __init__(self,session:SessionGenerator):
        print("UserRepository was initiated")
        self.session_generator=session

    async def add_user(self,entry:User)->int:
           async  for session in  self.session_generator.get_session():
            try:
                session.add(entry)
                await session.commit()
                return 200
            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400,detail=f"something went wrong while entring the new user {error}")


    async def get_user(self,user_name:str|None=None,email:str|None=None,user_id:uuid.UUID|None=None)->User:
           async  for session in  self.session_generator.get_session():
            try:
                if not  user_name and not email and not user_id:
                    raise HTTPException(status_code=400,detail="provide user_name or email or id")
                condition=[]
                if user_name:
                    condition.append(User.user_name==user_name)
                if email:
                        condition.append(User.email == email)
                if user_id:
                    condition.append(User.id == user_id)
                result=await session.execute(
                    select(User).where(and_(*condition))
                )
                return result.scalars().first()
            except Exception as error:
                await session.rollback()
                raise HTTPException(status_code=400,detail=f"something went wrong while entring the new user {error}")





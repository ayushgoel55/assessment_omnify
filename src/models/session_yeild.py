from src.utils.singleton import singleton
from abc import ABC,abstractmethod


class SessionGenerator(ABC):
    @abstractmethod
    async def get_session(self):
        pass




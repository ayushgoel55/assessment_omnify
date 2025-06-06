
from abc import ABC,abstractmethod
from typing import Any

class BaseMapper(ABC):
    @abstractmethod
    def map(self,inp:Any)->Any:
        pass
from abc import ABC,abstractmethod
from typing import Tuple,Any


class BaseValidator(ABC):
    @abstractmethod
    def validate(self,inp:Any)->Tuple[bool,list[Any]]:
        pass


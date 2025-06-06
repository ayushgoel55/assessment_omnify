from abc import ABC,abstractmethod
from typing import Any,Tuple


class BaseProcessor(ABC):
    @abstractmethod
    def process(self,inp:Any)->Tuple[bool,list[Any]]:
        pass
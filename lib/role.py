from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .participant import Participant


class Role(metaclass=ABCMeta):
    @abstractmethod
    async def night(self, participant: 'Participant'):
        pass

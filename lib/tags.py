from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from .death_cause import DeathCause

if TYPE_CHECKING:
    from .participant import Participant


class Tag(metaclass=ABCMeta):

    @abstractmethod
    async def can_die(self, participant: 'Participant', death_cause: 'DeathCause') -> bool:
        pass


from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role


class Participant(metaclass=ABCMeta):
    role: Role = None

    @abstractmethod
    async def night(self):
        await self.role.night(self)

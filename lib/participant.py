from typing import List

from .death_cause import DeathCause
from .role import Role
from .tags import Tag


class Participant(object):
    role: Role
    tags: List[Tag]

    async def night(self):
        await self.role.night(self)

    async def try_kill(self, death_cause: DeathCause) -> bool:
        if not all([await self.role.can_die(self, death_cause)] +
                   [await tag.can_die(self, death_cause) for tag in self.tags]):
            return False
        print('Killing participant')
        return True

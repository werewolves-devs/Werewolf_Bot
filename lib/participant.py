from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role


class Participant(object):
    role: Role = None

    async def night(self):
        await self.role.night(self)

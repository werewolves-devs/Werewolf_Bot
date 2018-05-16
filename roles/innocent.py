from lib.death_cause import DeathCause
from lib.participant import Participant
from lib.role import Role


class Innocent(Role):

    async def night(self, participant: 'Participant'):
        pass

    async def can_die(self, participant: 'Participant', death_cause: 'DeathCause') -> bool:
        return True

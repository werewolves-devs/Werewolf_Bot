from lib.death_cause import DeathCause
from lib.participant import Participant
from lib.role import Role
from lib.tags import Tag


class AmuletTag(Tag):

    async def can_die(self, participant: 'Participant', death_cause: 'DeathCause') -> bool:
        if isinstance(participant.role, AmuletHolder):
            return True
        # Can't use amulet twice.
        participant.tags.remove(self)
        return False


class AmuletHolder(Role):
    async def night(self, participant: 'Participant'):
        amulets = [isinstance(tag, AmuletTag) for tag in participant.tags]
        if len(amulets) > 0:
            await participant.secret_role_channel.send_message('Who do you want to give the amulet?')
            # and somehow get the answer. -> await

    async def can_die(self, participant: 'Participant', death_cause: 'DeathCause') -> bool:
        return True

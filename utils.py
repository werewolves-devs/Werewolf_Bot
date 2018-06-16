from typing import Union

import discord
from discord import Member, Role
from discord.ext import commands
from discord.ext.commands import CommandError, Context as CommandContext

from config import game_master as game_master_role, participant
from management.db import db_get


def has_role(member: Member, role: Union[Role, int, str]):
    if isinstance(role, Role):
        role = role.id
    role = int(role)
    return discord.utils.get(member.roles, id=role) is not None


def is_alive(member: Member) -> bool:
    return has_role(member, participant)


def is_active(member: Member) -> bool:
    """
    if a player is active, it means they are alive AND can do game actions like voting.

    one counter example are frozen players
    """
    return is_alive(member) and not db_get(member.id, 'frozen')


class GameMastersOnly(CommandError):
    pass


def is_game_master(member: Member) -> bool:
    return discord.utils.find(lambda role: role.id == int(game_master_role), member.roles) is not None


def game_masters_only():
    async def predicate(ctx: CommandContext):
        if not is_game_master(ctx.author):
            raise GameMastersOnly
        return True

    return commands.check(predicate)


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

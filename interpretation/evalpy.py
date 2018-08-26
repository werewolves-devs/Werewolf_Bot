import os
import re
from typing import List, Dict, Pattern

import discord
from discord import Embed, Color

REPLACEMENTS: Dict[Pattern, str] = {
    re.compile(r'<@!?(?P<id>[0-9]+)>'): '(guild.get_member({id}) if guild is not None else client.get_user({id}))',
    re.compile(r'<#(?P<id>[0-9]+)>'): '(discord.utils.get(all_channels, id={id}))',
    re.compile(r'<@&(?P<id>[0-9]+)>'): '(discord.utils.get(all_roles, id={id}))',
    # Maybe later emoji support
}


async def handle_eval(message: discord.Message, client: discord.Client, to_eval: str):
    channel: discord.TextChannel = message.channel
    author: discord.Member = message.author

    all_channels: List[discord.Guild] = []
    all_roles: List[discord.Role] = []
    for guild in client.guilds:
        guild: discord.Guild = guild  # for type hints
        all_channels += guild.channels
        all_roles += guild.roles

    variables = {
        'message': message,
        'author': author,
        'channel': channel,
        'all_channels': all_channels,
        'all_roles': all_roles,
        'client': client,
        'discord': discord,
        'os': os,
        'main_ww': main_ww,
        'print': (lambda *text: client.loop.create_task(channel.send(' '.join(text)))),
        'guild': channel.guild if hasattr(channel, 'guild') else None,
    }
    lines: List[str] = to_eval.strip().split('\n')
    lines[-1] = 'return ' + lines[-1]
    block: str = '\n'.join(' ' + line for line in lines)
    code = f"async def code({', '.join(variables.keys())}):\n" \
           f"{block}"

    for regex, replacement in REPLACEMENTS.items():
        code = re.sub(regex, lambda match: replacement.format(**match.groupdict()), code)

    _globals, _locals = {}, {}
    try:
        exec(code, _globals, _locals)
    except Exception as e:
        await message.channel.send(
            embed=discord.Embed(color=discord.Color.red(), description="Compiler Error: `%s`" % (str(e))))
        return
    result = {**_globals, **_locals}
    try:
        result = await result["code"](**variables)
    except Exception as e:
        await message.channel.send(
            embed=discord.Embed(color=discord.Color.red(), description="Runtime Error: `%s`" % (str(e))))
        return

    return await channel.send(
        embed=Embed(
            color=Color.red(),
            description="📥 Evaluation success: ```py\n%r\n```" % result))

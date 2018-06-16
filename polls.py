from typing import List

from discord import TextChannel, Guild, Member, Message, Embed, Color
from discord.ext import commands
from discord.ext.commands import Context as CommandContext
from tinydb import TinyDB, Query

from management.db import db_get
from utils import game_masters_only, is_active, chunks

db = TinyDB('polls.json').table('polls')

Poll = Query()


class PollCog(object):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    @game_masters_only()
    async def poll(self, ctx: CommandContext, title, *, description):
        channel: TextChannel = ctx.channel
        guild: Guild = ctx.guild
        users: List[Member] = [member for member in guild.members if is_active(member)]
        messages: List[Message] = []
        for user_list in chunks(users, 15):
            embed = Embed(
                color=Color(0x32CD32),
                title=title,
                description=description,
            )
            for user in user_list:
                embed.add_field(name=db_get(user.id, 'emoji'),
                                value=user.mention,
                                inline=True)
            message: Message = await channel.send(embed=embed)
            messages.append(message)
            for user in user_list:
                await message.add_reaction(db_get(user.id, 'emoji'))


def setup(bot):
    bot.add_cog(PollCog(bot))

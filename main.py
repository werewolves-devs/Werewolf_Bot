from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MissingRequiredArgument

import config
# Import config data
from config import prefix
from config import welcome_channel
from utils import GameMastersOnly

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

'''
To spare some time, the program should keep track of channels that it has sent messages in before.
This way, sending messages to the right channels should (hopefully) save some time,
as the bot doesn't need to ask the API for a channel for every message.
Instead, it should save a table with the channel objects.


no. they are cached anyway. it isnt a coroutine so it RUNS LOCALLY. PLEASE.
'''
channel_table = []


async def on_command_error(ctx: commands.Context, exc: BaseException):
    if isinstance(exc, CommandNotFound):
        await ctx.send(exc.args[0])
    if isinstance(exc, MissingPermissions):
        await ctx.send(
            embed=Embed(
                description='You need to be an admin to execute this command - sorry',
                color=Color.red()))
    if isinstance(exc, MissingRequiredArgument):
        await ctx.send(
            embed=Embed(
                color=Color.red(),
                description='You are missing a required argument: ' + str(exc.param)))
    if isinstance(exc, GameMastersOnly):
        await ctx.send(
            embed=Embed(
                description='This command is only for GMs. Sorry.',
                color=Color.red()))
    else:
        raise exc


client.on_command_error = on_command_error


# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.get_channel(welcome_channel).send('Beep boop! I just went online!')


client.load_extension('polls')

client.run(config.TOKEN)

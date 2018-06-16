from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MissingRequiredArgument
import discord
from discord import Embed, Color
import random
import asyncio


initial_extensions = ['conspiracy_channels.main',
                      'management.admin',
                      'polls']


# Import config data
from config import welcome_channel
from utils import GameMastersOnly
from config import prefix, welcome_channel, bot_spam
import config

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

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


bot.on_command_error = on_command_error
# Whenever the bot regains his connection with the Discord API.
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('--Reminder: You don\'t need to restart the bot to load new changes, just !reload the cog--')

    # Load extensions
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            await bot.get_channel(bot_spam).send('Error whilst loading module ' + extension + '\nErr: ```' + str(e) + '```\n\n*See the console for more details*')
            print(str(e))
    watching = discord.ActivityType.watching
    activity = discord.Activity(type=watching, name='Werewolves')
    await bot.change_presence(activity=activity)
    await bot.get_channel(welcome_channel).send('Beep boop! I just went online!')


bot.run(config.TOKEN)

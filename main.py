from discord.ext import commands
from discord import Embed, Color
import random
import asyncio


initial_extensions = ['conspiracy_channels.main',
                      'management.admin']


# Import config data
from config import prefix
import config

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

# Whenever a message is sent.
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return

# Whenever the bot regains his connection with the Discord API.
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    await bot.send_message(bot.get_channel(config.welcome_channel),'Beep boop! I just went online!')
    # Load extensions
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.command(name='Test')
async def test():
    print("Hi")


bot.run(config.TOKEN)

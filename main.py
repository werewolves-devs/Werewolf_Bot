from discord.ext import commands
from discord import Embed, Color
import random
import asyncio


initial_extensions = ['conspiracy_channels.main',
                      'management.admin']


# Import config data
from config import prefix, welcome_channel, bot_spam
import config

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

# Whenever the bot regains his connection with the Discord API.
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

    # Load extensions
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except:
            await bot.get_channel(bot_spam).send('Error whilst loading module ' + extension)
    await bot.get_channel(welcome_channel).send('Beep boop! I just went online!')

@bot.command(name='Test')
async def test():
    print("Hi")


bot.run(config.TOKEN)

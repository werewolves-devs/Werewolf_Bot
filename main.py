from discord.ext import commands
from discord import Embed, Color
import random
import asyncio


initial_extensions = ['conspiracy_channels.main',
                      'management.admin']


# Import config data
from config import prefix
import config

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
bot = client # Either one can be referred to, though I believe we should be using bot

# Whenever a message is sent.
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.send_message(client.get_channel(config.welcome_channel),'Beep boop! I just went online!')
    # Load extensions
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.command(name='Test')
async def test():
    print("Hi")


client.run(config.TOKEN)

from discord.ext import commands
import random
import asyncio

# Import config data
from config import prefix
import config

client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))

'''
To spare some time, the program should keep track of channels that it has sent messages in before.
This way, sending messages to the right channels should (hopefully) save some time,
as the bot doesn't need to ask the API for a channel for every message.
Instead, it should save a table with the channel objects.
'''
channel_table = []

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

    #await client.send_message(client.get_channel(welcome_channel),'Beep boop! I just went online!')
    # Testing
    bot.load_extension('conspiracy_channels.main')

client.run(config.TOKEN)

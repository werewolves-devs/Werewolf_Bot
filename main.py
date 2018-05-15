import discord
import random
import asyncio

# Import config data
from config import prefix
import config

client = discord.Client()


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.send_message(client.get_channel(welcome_channel),'Beep boop! I just went online!')

client.run(config.TOKEN)

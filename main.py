import discord
import random
import asyncio

TOKEN = 'this_is_where_your_token_goes_buddy'

client = discord.Client()


# List of specific files

# List of specific channels

# List of specific roles
game_master = # TODO
participant = #TODO
dead_participant = #TODO
frozen_participant = #TODO
suspended = #TODO



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

client.run(TOKEN)

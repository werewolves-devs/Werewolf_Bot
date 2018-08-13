# This file controls a seperate bot, but for some reason Randium wants it in the same directory with the same config file specified (?)
# Anyhow, here it is

import discord
import asyncio
import datetime

# Import config data
from config import universal_prefix as prefix, TOKEN as token, bot_spam

client = discord.Client()

async def check_time():
    print('   | > Waiting for client to be ready')
    await client.wait_until_ready()
    print('   | > Event loop triggered')
    await asyncio.sleep(1)
    while True:
        time = datetime.datetime.now()
        if str(time.minute) == "0":
            print("--> We've reached the hour! It's now %s00 hours." % (time.hour))
        if str(time.minute) == "0" and str(time.hour) == "8":
            await client.get_channel(bot_spam).send(prefix + "day")
        if str(time.minute) == "0" and str(time.hour) == "21":
            await client.get_channel(bot_spam).send(prefix + "night")
        await asyncio.sleep(45)

# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print(' --> Logged in as')
    print('   | > ' + client.user.name)
    print('   | > ' + str(client.user.id))

    await client.get_channel(int(bot_spam)).send('Heyo, ya boi online!')

print(' --> Please wait whilst we start up background tasks ...')
client.loop.create_task(check_time())
print(' --> Please wait whilst we connect to the Discord API...')
client.run(token)

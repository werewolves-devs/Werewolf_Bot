# This file controls a seperate bot, but for some reason Randium wants it in the same directory with the same config file specified (?)
# Anyhow, here it is

import management.dynamic as dy
import management.db as db
import discord
import asyncio
import datetime

# Import config data
from config import universal_prefix as prefix, TM_TOKEN as token, bot_spam, activity_hours, welcome_channel
from management.shop import age_shop

client = discord.Client()

async def check_time():
    print('   | > Waiting for client to be ready')
    await client.wait_until_ready()
    print('   | > Event loop triggered')
    await asyncio.sleep(1)

    while True:
        time = datetime.datetime.now()


        # Give the hour signal
        if str(time.minute) == "0":
            print("--> We've reached the hour! It's now %s00 hours." % (time.hour))

            # Set each user's activity one up.
            for user in db.player_list():
                activity = db.db_get(user,'activity')
                db.db_set(user,'activity',activity + 1)

                if db.isParticipant(user):
                    if activity_hours - activity == 24:
                        await client.get_channel(bot_spam).send(prefix + "warn <@{}>".format(user))
                    elif activity >= activity_hours:
                        await client.get_channel(bot_spam).send(prefix + "idle <@{}>".format(user))
        
            # Set each shop's age one up.
            age_shop()

            # Give the day signal
            if str(time.hour) == "8":
                if dy.get_stage() != "NA":
                    print('Another day has started!')
                    await client.get_channel(bot_spam).send(prefix + "pay")
                    await asyncio.sleep(45)
                    await client.get_channel(bot_spam).send(prefix + "day")
                else:
                    await client.get_channel(bot_spam).send("Beep boop! Another day has begun!")

            # Give the night signal
            if str(time.hour) == "21":
                if dy.get_stage() != "NA":
                    print('Another night has begun!')
                    await client.get_channel(bot_spam).send(prefix + "pight")
                    await asyncio.sleep(45)
                    await client.get_channel(bot_spam).send(prefix + "night")
                else:
                    await client.get_channel(bot_spam).send("Beep boop! The night has started!")

            await asyncio.sleep(45)

        await asyncio.sleep(45)


# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print(' --> Logged in as')
    print('   | > ' + client.user.name)
    print('   | > ' + str(client.user.id))

    await client.get_channel(int(welcome_channel)).send('Heyo, ya boi online!')

print(' --> Please wait whilst we start up background tasks ...')
client.loop.create_task(check_time())
print(' --> Please wait whilst we connect to the Discord API...')
client.run(token)

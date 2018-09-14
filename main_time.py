# This file controls a seperate bot, but for some reason Randium wants it in the same directory with the same config file specified (?)
# Anyhow, here it is

import management.roulette as roulette
import management.dynamic as dy
import management.db as db
import discord
import asyncio
import datetime
import config
import os

# Import config data
from shutil import copy
from config import universal_prefix as prefix, TM_TOKEN as token, bot_spam, activity_hours, welcome_channel
from interpretation.check import is_command
from management.shop import age_shop
from management.general import purge_activity, deal_credits


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

            # Purge activity
            purge_activity()

            # Give free credits in the middle of the night.
            if str(time.hour) == "0":
                await client.get_channel(welcome_channel).send('Gonna send some credits! Get ready!')
                deal_credits()

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

            # Make a backup of the database
            newpath = 'backup/{}_{}/{}_{}h/'.format(time.year,time.month,time.day,time.hour)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            open('backup/{}_{}/{}_{}h/{}_backup_game.db'.format(time.year,time.month,time.day,time.hour,time.minute), 'a').close()
            open('backup/{}_{}/{}_{}h/{}_backup_general.db'.format(time.year,time.month,time.day,time.hour,time.minute), 'a').close()
            open('backup/{}_{}/{}_{}h/{}_backup_stats.json'.format(time.year,time.month,time.day,time.hour,time.minute), 'a').close()
            open('backup/{}_{}/{}_{}h/{}_backup_dynamic.json'.format(time.year,time.month,time.day,time.hour,time.minute), 'a').close()
            open('backup/{}_{}/{}_{}h/{}_backup_config.py'.format(time.year,time.month,time.day,time.hour,time.minute), 'a').close()
            copy(config.database,'backup/{}_{}/{}_{}h/{}_backup_game.db'.format(time.year,time.month,time.day,time.hour,time.minute))
            copy(config.general_database,'backup/{}_{}/{}_{}h/{}_backup_general.db'.format(time.year,time.month,time.day,time.hour,time.minute))
            copy(config.stats_file,'backup/{}_{}/{}_{}h/{}_backup_stats.json'.format(time.year,time.month,time.day,time.hour,time.minute))
            copy(config.dynamic_config,'backup/{}_{}/{}_{}h/{}_backup_dynamic.json'.format(time.year,time.month,time.day,time.hour,time.minute))
            copy('config.py','backup/{}_{}/{}_{}h/{}_backup_config.py'.format(time.year,time.month,time.day,time.hour,time.minute))

            await asyncio.sleep(45)

        await asyncio.sleep(10)
        roulette.surrender(True)

# Whenever a message is sent.
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    time = datetime.datetime.now()

    if is_command(message, ['time','whattime', 'what time'], False, '') or is_command(message, ['time','whattime', 'what time'], True, ''):
        await message.channel.send("It's currently {}:{}.".format(time.hour,time.minute))

        if int(time.hour) > 7 and int(time.hour) < 21:
            await message.channel.send("That's {} hours and {} minutes left till the night starts.".format(20-time.hour,59-time.minute))
        else:
            await message.channel.send("That's {} hours and {} minutes left until the morning starts.".format((31-time.hour)%24,59-time.minute))


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

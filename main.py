import discord
import random
import asyncio

# Import config data
from config import prefix
from management.db import db_set
from interpretation.ww_head import process
import config


client = discord.Client()


# Whenever a message is sent.
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    # Check if the message author has the Game Master role
    isGameMaster = False
    if False:
        isGameMaster = True

    result = process(message,isGameMaster)

    temp_msg = []

    gamelog_channel = client.get_channel(config.game_log)
    botspam_channel = client.get_channel(config.bot_spam)
    storytime_channel = client.get_channel(config.story_time)

    for mailbox in result:

        for element in mailbox.gamelog:
            msg = await client.send_message(gamelog_channel,element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.botspam:
            msg = await client.send_message(botspam_channel,element.content)
            if element.temporary == True:
                temp_msg.append(msg)
        
        for element in mailbox.storytime:
            msg = await client.send_message(storytime_channel,element.content)
            if element.temporary == True:
                temp_msg.append(msg)
        
        for element in mailbox.channel:
            msg = await client.send_message(client.get_channel(element.destination),element.content)
            if element.temporary == True:
                temp_msg.append(msg)
        
        for element in mailbox.player:
            msg = await client.send_message('''How did we do this again?''',element.content)
            if element.temporary == True:
                temp_msg.append(msg)
        
        for element in mailbox.oldchannels:
            # element.channel - channel to be edited;
            # element.victim - person's permission to be changed;
            # element.number - type of setting to set to:
                # 0 - no access     (no view, no type)
                # 1 - access        (view + type)
                # 2 - frozen        (view, no type)
                # 3 - abducted      (no view, no type)
                # 4 - dead          (dead role?)
            
            # TODO
            pass

        for element in mailbox.newchannels:
            # element.name - name of the channel;
            # element.owner - owner of the channel;
            #
            # @Participant      - no view + type
            # @dead Participant - view + no type
            # @everyone         - no view + no type

            # All you need to do is create a channel where only the channel owner has access.
            # The other members are given access through another Mailbox.
            # You could make the work easier if you also posted a cc channel message already over here.

            # TODO

            for buddy in element.settlers:
                db_set(buddy,"channel",'''id of the channel you just created''')
    
    # Delete all temporary messages after "five" seconds.
    await asyncio.sleep(5)
    for msg in temp_msg:
        await delete_message(msg)


# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    await client.send_message(client.get_channel(welcome_channel),'Beep boop! I just went online!')

client.run(config.TOKEN)

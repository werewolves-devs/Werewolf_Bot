'''

888       888                                                  888  .d888       888888b.            888    
888   o   888                                                  888 d88P"        888  "88b           888    
888  d8b  888                                                  888 888          888  .88P           888    
888 d888b 888  .d88b.  888d888  .d88b.  888  888  888  .d88b.  888 888888       8888888K.   .d88b.  888888 
888d88888b888 d8P  Y8b 888P"   d8P  Y8b 888  888  888 d88""88b 888 888          888  "Y88b d88""88b 888    
88888P Y88888 88888888 888     88888888 888  888  888 888  888 888 888          888    888 888  888 888    
8888P   Y8888 Y8b.     888     Y8b.     Y88b 888 d88P Y88..88P 888 888          888   d88P Y88..88P Y88b.  
888P     Y888  "Y8888  888      "Y8888   "Y8888888P"   "Y88P"  888 888          8888888P"   "Y88P"   "Y888 
                                                                                                           
                         - = https://github.com/werewolves-devs/werewolf bot = -
                                                                                                           
'''

import discord
import random
import asyncio

# Import config data
from config import prefix, welcome_channel
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
    if False: # somebody fix this
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
            # element.members - members to be added to the channel [NEEDS TO BE MADE YET]
            #
            # @Participant      - no view + type
            # @dead Participant - view + no type
            # @everyone         - no view + no type

            # All you need to do is create a channel where only the channel owner has access.
            # The other members are given access through another Mailbox.
            # You could make the work easier if you also posted a cc channel message already over here.

            # TODO

            if not message_author in element.members:
                element.members.append(message_author)

            message = creation_messages.cc_intro(member_ids)
            
            # Role objects (based on ID)
            main_guild = client.get_channel(bot_spam).guild # Find the guild we're in
            roles = main_guild.roles # Roles from the guild
            game_master_role = discord.utils.find(lambda r: r.id == game_master, roles) #WUSDIS                     # \
            dead_participant_role = discord.utils.find(lambda r: r.id == dead_participant, roles) #WUSDIS           # | Find various role objects
            frozen_participant_role = discord.utils.find(lambda r: r.id == frozen_participant, roles) #WUSDIS       # /
            default_permissions = {
                main_guild.default_role: discord.PermissionOverwrite(read_messages=False),                     # \
                frozen_participant_role: discord.PermissionOverwrite(send_messages=False),                     # |
                dead_participant_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),   # | Set the permissions for each role and the bot user
                game_master_role: discord.PermissionOverwrite(read_messages=True),                             # |
                self.bot.user: discord.PermissionOverwrite(read_messages=True),                                # /
                **{                                                                                       # \
                    member: discord.PermissionOverwrite(read_messages=True) for member in element.members # | Set permissions for each member
                },                                                                                        # /
            }

            with open("conspiracy_channels/cc_data.json") as cc_data:
                try:
                    data = json.load(cc_data) # Try to load conspiracy channel data from a file, ./cc_data.json
                except JSONDecodeError:
                    return await client.get_channel(message.channel).send('cc_data was not found or is invalid.') # If we can't find it or it's invalid, throw an error
            try:
                category = client.get_channel(data['category_id']) # Find the category based on the data from cc_data
            except:
                #Category couldn't be found, let's make a new one
                category = await main_guild.create_category('Conspiracy Channels', reason='Old CC Category not found; Creating new one') # TODO: Include season code etc
            if len(category.channels) > 49:
                # Current category is full, make a new one!
                category = await main_guild.create_category('Conspiracy Channels', reason='Old CC Category full; Creating new one') # TODO: Include season code etc
            try:
                try:
                    channel = await ctx.guild.create_text_channel( # Create a text channel
                        name, # With the name 'name'
                        category=category, # In the category 'category' (A variable we just defined earlier)
                        overwrites=default_permissions, # Set the permissions to the 'default_permissions' object we created earlier
                        reason='Conspiracy Channel creation requested by ' + ctx.author.mention) # Set the reason for the Audit Log
                    await channel.send(message) # Send our welcome message from cc_intro
                except Exception as e: # Catch any thrown exceptions and send an error to the user
                    await ctx.channel.send('There was an error creating the channel, likely role finding. Please contact a Game Master for more info.\n\n*Game Masters: Check the console*')
                    raise e # Send the full info to console
            except Exception as e:
                # Something went wrong. Let's tell the user.
                ctx.message.channel.send("Something went wrong. Please contact a Game Master for additional assistance.\n\n*Game Masters: Check the console*")
                raise e

            data['category_id'] = category.id
            with open("conspiracy_channels/cc_data.json", 'w') as cc_data:
                json.dump(data, cc_data) # Rewrite our 'data' back to disk, as it may have been modified
            
            for buddy in element.settlers:
                db_set(buddy,"channel",'''id of the channel you just created''')

    # Delete all temporary messages after "five" seconds.
    await asyncio.sleep(5)
    for msg in temp_msg:
        await client.delete_message(msg)


# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    await client.send_message(client.get_channel(welcome_channel),'Beep boop! I just went online!')

client.run(config.TOKEN)

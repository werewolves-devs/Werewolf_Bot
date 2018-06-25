'''

888       888                                                  888  .d888       888888b.            888    
888   o   888                                                  888 d88P"        888  "88b           888    
888  d8b  888                                                  888 888          888  .88P           888    
888 d888b 888  .d88b.  888d888  .d88b.  888  888  888  .d88b.  888 888888       8888888K.   .d88b.  888888 
888d88888b888 d8P  Y8b 888P"   d8P  Y8b 888  888  888 d88""88b 888 888          888  "Y88b d88""88b 888    
88888P Y88888 88888888 888     88888888 888  888  888 888  888 888 888          888    888 888  888 888    
8888P   Y8888 Y8b.     888     Y8b.     Y88b 888 d88P Y88..88P 888 888          888   d88P Y88..88P Y88b.  
888P     Y888  "Y8888  888      "Y8888   "Y8888888P"   "Y88P"  888 888          8888888P"   "Y88P"   "Y888 
                                                                                                           
                         - = https://github.com/werewolves-devs/werewolf_bot = -
                                                                                                           
'''

import discord
import random
import asyncio

# Import config data
import story_time.cc_creation as creation_messages
from config import prefix, welcome_channel
from management.db import db_set, db_get
from interpretation.ww_head import process
import config
import management.db as db


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

    gamelog_channel = client.get_channel(int(config.game_log))
    botspam_channel = client.get_channel(int(config.bot_spam))
    storytime_channel = client.get_channel(int(config.story_time))

    for mailbox in result:

        for element in mailbox.gamelog:
            msg = await gamelog_channel.send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.botspam:
            msg = await botspam_channel.send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.storytime:
            msg = await storytime_channel.send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.answer:
            msg = await message.channel.send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.channel:
            msg = await client.get_channel(element.destination).send(element.content)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.player:
            msg = await client.get_channel('''How did we do this again?''').send(element.content)
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
            # element.members - members of the channel
            # element.settlers - members for whom this shall become their home channel
            #
            # @Participant      - no view + type
            # @dead Participant - view + no type
            # @everyone         - no view + no type

            # All you need to do is create a channel where only the channel owner has access.
            # The other members are given access through another Mailbox.
            # You could make the work easier if you also posted a cc channel message already over here.

            if ' ' not in element.name:

                if element.owner not in element.members:
                    element.members.append(element.owner)
                for buddy in element.settlers:
                    if buddy not in element.members:
                        msg = """**Warning:** I'm adding settlers to a channel!\nThis is should not be a problem, \
                        but it does at least indicate a flaw in the bot's code. Please, report this to the Game Masters!"""
                        await client.get_channel(message.channel).send(msg)
                        element.members.append(buddy)

                intro_msg = creation_messages.cc_intro(element.members)

                viewers = []
                abductees = []
                for member in db.player_list():
                    if db_get(member,'abducted') == 1:
                        abductees.append(member)
                    else:
                        if member in element.members or db_get(member,'role') in ['Dead','Spectator']:
                            viewers.append(member)

                # Role objects (based on ID)
                main_guild = botspam_channel.guild # Find the guild we're in
                roles = main_guild.roles # Roles from the guild
                game_master_role = discord.utils.find(lambda r: r.id == game_master, roles)
                dead_participant_role = discord.utils.find(lambda r: r.id == dead_participant, roles)
                frozen_participant_role = discord.utils.find(lambda r: r.id == frozen_participant, roles)
                default_permissions = {
                    main_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    frozen_participant_role: discord.PermissionOverwrite(send_messages=False),
                    dead_participant_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
                    game_master_role: discord.PermissionOverwrite(read_messages=True),
                    client.user: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                    **{
                        member: discord.PermissionOverwrite(read_messages=True) for member in viewers
                    },
                }

                # Create a new category if needed
                if db.get_category() == None:
                    category = await main_guild.create_category('CC part {}'.format(db.count_categories(), reason='It seems like we couldn\'t use our previous category! Don\'t worry, I just created a new one.')
                    db.add_category(category)
                else:
                    category = db.get_category()

                try:
                    # Create the text channel
                    channel = await main_guild.create_text_channel(
                        name="s{}_".format(config.season) + element.name,
                        category=category,
                        overwrites=default_permissions,
                        reason='CC requested by ' + message.author.mention)
                    db.add_channel(channel.id,element.owner)
                    await channel.send(intro_msg)

                    # Set all access rules in the database
                    for victim in abductees:
                        db.set_user_in_channel(channel.id,victim,3)
                    for user in viewers:
                        if db_get(user,'role') in ['Dead','Spectator']:
                            db.set_user_in_channel(channel.id,user,4)
                        elif db_get(user,'frozen') == 1:
                            db.set_user_in_channel(channel.id,user,2)
                        else:
                            db.set_user_in_channel(channel.id,user,1)

                except Exception as e: # Catch any thrown exceptions and send an error to the user.
                    await message.channel.send('It seems like I\'ve encountered an error! Please let the Game Masters know about this!')
                    await botspam_channel.send("Oi, Game Masters! I got a problem concerning channel creation for ya to fix.")
                    botspam_channel.send(e)
                    raise e # Send the full log to Buddy1913 and his sketchy VM.

                # Give the settlers their own happy little residence
                for buddy in element.settlers:
                    db_set(buddy,"channel",channel.id)
            
            else:
                """This should not happen, but we'll use it, to prevent the bot from purposely causing an error
                everytime someone attempts to create a channel that contains spaces. 'cause believe me,
                that happens ALL the time."""
                msg = await message.channel.send("I\'m terribly sorry, but you can\'t use spaces in your channel name. Try again!")
                temp_msg.append(msg)


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

ascii = '''

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

splashes = [
'Now with 100% less JavaScript',
'I made it, we *HAVE* to use it',
'Standards? What are they?',
'Nah, we don\'t use libraries here.',
'The mailbox system is a \'good idea\'',
'Leaking tokens is fun!',
'Let\'s just shove everything into main.py, who still does organization in 2018',
'Works on my machine',
'Always use a database. What\'s a JSON?',
'Powered by Electricity',
'Who still writes docs in 2018?',
"First normal form? What does that mean?",
"By using a relational database but with nonrelational practices we get the worst of both worlds!"
]

import discord
import random
import asyncio

# Import config data
import story_time.cc_creation as creation_messages
from config import prefix, welcome_channel, game_master, dead_participant, game_master, frozen_participant
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

    gamelog_channel = client.get_channel(int(config.game_log))
    botspam_channel = client.get_channel(int(config.bot_spam))
    storytime_channel = client.get_channel(int(config.story_time))

    # Check if the message author has the Game Master role
    isGameMaster = False
    if message.guild == gamelog_channel.guild:
        if game_master in [y.id for y in message.author.roles]:
            isGameMaster = True

    result = process(message,isGameMaster)

    temp_msg = []

    for mailbox in result:

        for element in mailbox.gamelog:
            msg = await gamelog_channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.botspam:
            msg = await botspam_channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.storytime:
            msg = await storytime_channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.answer:
            msg = await message.channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        for element in mailbox.channel:
            if element.embed:
                msg = await client.get_channel(int(element.destination)).send(embed=element.content)
                for emoji in element.reactions:
                    await msg.add_reaction(emoji)
                if element.temporary == True:
                    temp_msg.append(msg)
            else:
                msg = await client.get_channel(int(element.destination)).send(element.content)
                for emoji in element.reactions:
                    await msg.add_reaction(emoji)
                if element.temporary == True:
                    temp_msg.append(msg)

        for element in mailbox.player:
            member = client.get_user(element.destination)
            if member == None:
                await message.channel.send("Couldn't send a DM to <@{}>!".format(element.destination))
                await botspam_channel.send("<@{}> has attempted to send a DM to <@{}>, but failed, because we couldn't find the specified user via `get_user`.".format(message.author.id,element.destination))
            else:
                msg = await member.send(element.content)
                for emoji in element.reactions:
                    await msg.add_reaction(emoji)
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

                main_guild = botspam_channel.guild # Find the guild we're in

                if element.owner not in element.members:
                    element.members.append(element.owner)
                for buddy in element.settlers:
                    if buddy not in element.members:
                        msg = """**Warning:** I'm adding settlers to a channel!\nThis is should not be a problem, \
                        but it does at least indicate a flaw in the bot's code. Please, report this to the Game Masters!"""
                        await client.get_channel(message.channel).send(msg)
                        element.members.append(buddy)

                viewers = []
                abductees = []
                for member in db.player_list():
                    if db_get(member,'abducted') == 1 and member in element.members:
                        abductees.append(member)
                    elif member in element.members or db_get(member,'role') in ['Dead','Spectator'] or int(member) == int(element.owner):
                        if main_guild.get_member(int(member)) != None:
                            viewers.append(main_guild.get_member(int(member)))
                        else:
                            sorry = await message.channel.send("It doesn't seem like <@{}> is part of this server! I am sorry, I can't add them to your channel.".format(member))
                            temp_msg.append(sorry)

                intro_msg = creation_messages.cc_intro([v.id for v in viewers])

                # Role objects (based on ID)
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
                    category = await main_guild.create_category('CC part {}'.format(db.count_categories()), reason='It seems like we couldn\'t use our previous category! Don\'t worry, I just created a new one.')
                    db.add_category(category.id)
                else:
                    category = main_guild.get_channel(db.get_category())

                try:
                    # Create the text channel
                    reason_msg = 'CC requested by ' + message.author.name
                    channel = await main_guild.create_text_channel(
                        name="s{}_{}".format(config.season,element.name),
                        category=category,
                        overwrites=default_permissions,
                        reason=reason_msg)
                    db.add_channel(channel.id,element.owner)
                    await channel.send(intro_msg)

                    # Set all access rules in the database
                    for victim in abductees:
                        db.set_user_in_channel(channel.id,victim,3)
                    for user in viewers:
                        if db_get(user.id,'role') in ['Dead','Spectator']:
                            db.set_user_in_channel(channel.id,user.id,4)
                        elif db_get(user.id,'frozen') == 1:
                            db.set_user_in_channel(channel.id,user.id,2)
                        else:
                            db.set_user_in_channel(channel.id,user.id,1)

                except Exception as e: # Catch any thrown exceptions and send an error to the user.
                    await message.channel.send('It seems like I\'ve encountered an error! Please let the Game Masters know about this!')
                    await botspam_channel.send("Oi, Game Masters! I got a problem concerning channel creation for ya to fix.")
                    await botspam_channel.send(e)
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
        await msg.delete()


# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print(' --> Logged in as')
    print('   | > ' + client.user.name)
    print('   | > ' + str(client.user.id))

    await client.get_channel(welcome_channel).send('Beep boop! I just went online!')

print(ascii)
print(' --> "' + random.choice(splashes) + '"')
print(' --> Please wait whilst we connect to the Discord API...')
client.run(config.TOKEN)

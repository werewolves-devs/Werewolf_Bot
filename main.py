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
"By using a relational database but with nonrelational practices we get the worst of both worlds!",
"I haven\'t paid attention or read any comments, therefor it\'s impossible to understand!",
"Don\'t use that! Oh, you\'re asking why? Well... just don\'t it.",
"I don\'t wanna explain, just Google it.",
"What are cogs?",
"This is MY project. You\'re just freeloaders.",
"You've got three weeks to fix EVERYTHING.",
"No-one agrees? Too bad! My idea it is.",
"The next version will be written in Java only!"
]

import discord
import random
import asyncio

# Import config data
import story_time.cc_creation as creation_messages
from config import welcome_channel, game_master, dead_participant, frozen_participant, administrator
from config import ww_prefix as prefix
from management.db import db_set, db_get
from interpretation.ww_head import process
from interpretation.polls import count_votes
import config
import management.db as db


client = discord.Client()

async def remove_all_game_roles(member):
    for role in member.roles:
        if role.id == config.frozen_participant:
            await member.remove_roles(role, reason="Updating CC permissions")
        if role.id == config.dead_participant:
            await member.remove_roles(role, reason="Updating CC permissions")
        if role.id == config.suspended:
            await member.remove_roles(role, reason="Updating CC permissions")

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
        if game_master in [y.id for y in message.guild.get_member(message.author.id).roles]:
            isGameMaster = True

    isAdmin = False
    if message.guild == gamelog_channel.guild:
        if administrator in [y.id for y in message.guild.get_member(message.author.id).roles]:
            isAdmin = True

    result = process(message,isGameMaster,isAdmin)

    temp_msg = []

    for mailbox in result:

        if mailbox.evaluate_polls == True:
            for poll in db.get_all_polls():
                # poll.msg_table -> list of message ids
                # poll.blamed -> name of killer
                # poll.purpose -> the reason of the kill

                poll_channel = client.get_channel(int(poll.channel))
                if poll_channel == None:
                    await botspam_channel.send("We got a problem! Could you send these results to the appropriate channel, please?")
                    poll_channel = botspam_channel

                user_table = []
                for msg in poll.msg_table:
                    poll_msg = await poll_channel.get_message(msg)
                    for emoji in poll_msg.reactions:
                        users = await emoji.users().flatten()

                        for person in users:
                            if db.isParticipant(person.id):
                                user_table.append([person.id,emoji.emoji])

                log, result, chosen_emoji = count_votes(user_table,poll.purpose)

                await gamelog_channel.send(log)
                await poll_channel.send(result)

                chosen_one = db.emoji_to_player(chosen_emoji)

                if chosen_emoji != '' and chosen_one != None:
                    if poll.purpose == 'lynch':
                        db.add_kill(chosen_one,'Innocent')
                    elif poll.purpose == 'Mayor':
                        # TODO: give Mayor role and add data to dynamic.json
                        pass
                    elif poll.purpose == 'Reporter':
                        # TODO: give Reporter role and add data to dynamic.json
                        pass
                    elif poll.purpose == 'wolf':
                        db.add_kill(chosen_one,'Werewolf',db.random_wolf())
                    elif poll.purpose == 'cult':
                        db.add_kill(chosen_one,'Cult Leader',db.random_cult())
                    elif poll.purpose == 'thing':
                        # TODO: kill poor victim
                        pass


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
                if element.destination == "spam":
                    msg = await botspam_channel.send(embed=element.content)
                    for emoji in element.reactions:
                        await msg.add_reaction(emoji)
                    if element.temporary == True:
                        temp_msg.append(msg)
                else:
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

            # 0 -> read = False
            # 1 -> read = True
            # 2 -> give frozen (if they don't have it yet)
            # 3 -> read = False
            # 4 -> give dead role + remove participant role
            # 5 -> mute
            # 6 -> also mute, no read

            channel = client.get_channel(element.channel)
            user = client.get_user(element.victim)
            main_guild = botspam_channel.guild
            # member =main_guild.get_member(element.victim)
            member = main_guild.get_member(element.victim)
            await remove_all_game_roles(member)
            if element.number == 0:
                await channel.set_permissions(user, read_messages=False, send_messages=False)
            elif element.number == 1:
                await channel.set_permissions(user, read_messages=True, send_messages=True)
            elif element.number == 2 or element.number == 5:
                await channel.set_permissions(user, read_messages=True, send_messages=False)
            elif element.number == 3:
                await channel.set_permissions(user, read_messages=False, send_messages=False)
            elif element.number == 4:
                await channel.set_permissions(user, read_messages=True, send_messages=False)
            elif element.number == 6:
                await channel.set_permissions(user, read_messages=False, send_messages=False)
            else:
                await msg.channel.send('Something went wrong! Please contact a Game Master.')
                return
            if db.isParticipant(element.victim,True,True):
                db.set_user_in_channel(element.channel,element.victim,element.number)


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
                frozones = []
                abductees = []
                deadies = []
                for user in element.members:
                    member = main_guild.get_member(user)

                    if member == None:
                        await message.author.send("It doesn't seem like <@{}> is part of the server! I am sorry, I can't add them to your **conspiracy channel**.".format(user))
                    elif db.isParticipant(user,False,True) == True:
                        if int(db_get(user,'abducted')) == 1:
                            abductees.append(member)
                        elif int(db_get(user,'frozen')) == 1:
                            frozones.append(member)
                        elif db.isParticipant(user,False,False) == False:
                            deadies.append(member)
                        else:
                            viewers.append(member)
                    else:
                        deadies.append(member)

                intro_msg = creation_messages.cc_intro([v.id for v in viewers])

                # Role objects (based on ID)
                roles = main_guild.roles # Roles from the guild
                game_master_role = discord.utils.find(lambda r: r.id == game_master, roles)
                default_permissions = {
                    main_guild.default_role: discord.PermissionOverwrite(read_messages=False,send_messages=False),
                    game_master_role: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                    client.user: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                    **{
                        member: discord.PermissionOverwrite(read_messages=True,send_messages=True) for member in viewers
                    },
                    **{
                        member: discord.PermissionOverwrite(read_messages=True,send_messages=False) for member in frozones
                    },
                    **{
                        member: discord.PermissionOverwrite(read_messages=True,send_messages=False) for member in deadies
                    }
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
                    for member in viewers:
                        db.set_user_in_channel(channel.id,member.id,1)
                    for member in frozones:
                        db.set_user_in_channel(channel.id,member.id,2)
                    for member in abductees:
                        db.set_user_in_channel(channel.id,member.id,3)
                    for member in deadies:
                        if db.isParticipant(member.id,True,True) == True:
                            db.set_user_in_channel(channel.id,member.id,4)


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

        for element in mailbox.polls:
            # element.channel
            # element.purpose
            # element.user_id
            # element.description

            msg = element.description + '\n'
            emoji_table = []
            msg_table = []
            i = 0

            for user in db.poll_list():
                if db.isParticipant(int(user[0])):
                    i += 1
                    msg += user[1] + " - <@" + str(user[0]) + "> "

                    if int(user[2]) + int(user[3]) > 0:
                        if int(user[2]) == 1:
                            msg += "**[FROZEN]** "
                        if int(user[3]) == 1:
                            msg += "**[ABDUCTED] **"
                    else:
                        emoji_table.append(user[1])

                    if i % 20 == 19:
                        msg = await client.get_channel(element.channel).send(msg)
                        for emoji in emoji_table:
                            await msg.add_reaction(emoji)
                        msg_table.append(msg)
                        msg = ''
                    else:
                        msg += '\n'

            if msg != '':
                msg = await client.get_channel(element.channel).send(msg)
                for emoji in emoji_table:
                    await msg.add_reaction(emoji)
                msg_table.append(msg)
            db.add_poll(msg_table,element.purpose,element.channel,element.user_id)
            await botspam_channel.send("A poll has been created in <#{}>!".format(element.channel))

        for element in mailbox.deletecategories:
            id = element.channel
            category = client.get_channel(id)
            if category != None:
                bot_message = await message.channel.send('Please react with 👍 to confirm deletion of category `' + category.name + '`.\n\nNote: This action will irrevirsibly delete all channels contained within the specified category. Please use with discretion.')
                await bot_message.add_reaction('👍')
                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) == '👍'
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await message.channel.send('Confirmation timed out.')
                else:
                    await message.channel.send('Ok, I\'ll get right on that.\n\n*This might take some time.*')
                    for channel in category.channels:
                        await channel.delete()
                    await category.delete()
                    await message.channel.send('\n:thumbsup: Channels and category deleted')
            else:
                await message.channel.send('Sorry, I couldn\'t find that category.')

    # Delete all temporary messages after "five" seconds.
    await asyncio.sleep(120)
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
try:
    client.run(config.TOKEN)
except:
    print('   | > Error logging in. Check your token is valid and you are connected to the Internet.')

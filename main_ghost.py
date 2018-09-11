splash = '''

==========================================================
G H O S T B O T
==========================================================
WHAM! SUPER BIG AND IMPRESSIVE AND STUFF!
I DON'T HAVE ASCII ART!
DAYUM, THAT'S IMPRESSIVE!

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
'First normal form? What does that mean?',
'By using a relational database with nonrelational practices we get the worst of both worlds!',
'I haven\'t paid attention or read any comments, therefore it\'s impossible to understand!',
'Don\'t use that! Oh, you\'re asking why? Well... just don\'t it.',
'I don\'t wanna explain, just Google it.',
'What are cogs?',
'This is MY project. You\'re just freeloaders.',
'You\'ve got three weeks to fix EVERYTHING.',
'No-one agrees? Too bad! My idea it is.',
'The next version will be written in Java only!'
]

import discord
import random
import asyncio

# Import config data
# Imports go (folder name).(file name)
import story_time.cc_creation as creation_messages
import story_time.powerup as secret_messages
from config import welcome_channel, game_master, dead_participant, frozen_participant, administrator, peasant
from config import ghost_prefix as prefix
from management.db import db_set, db_get
from interpretation.ghost_head import process
from interpretation.polls import count_votes
from interpretation.basecode import create_token
import config
import random
import shop
import stats
import management.db as db
import management.dynamic as dy
import management.shop as db_shop
import management.general as general
import management.boxes as box
from emoji import emojize


client = discord.Client()

def get_role(server_roles, target_id):
    for each in server_roles:
       if each.id == target_id:
           return each
    return None

async def remove_all_game_roles(member):
    for role in member.roles:
        if role.id == config.frozen_participant:
            await member.remove_roles(role, reason="Updating CC permissions")
        if role.id == config.dead_participant:
            await member.remove_roles(role, reason="Updating CC permissions")
        if role.id == config.suspended:
            await member.remove_roles(role, reason="Updating CC permissions")
        if role.id == config.participant:
            await member.remove_roles(role, reason="Updating CC permissions")

already_quoted = []

@client.event
async def on_reaction_add(reaction, user):
    if user != client.user and db_shop.is_shop(reaction.message.id):
        # For shop
        bought_item = await shop.find_item_from_key("emoji", reaction.emoji, reaction.message.id)
        await reaction.message.remove_reaction(reaction.emoji, user)
        await reaction.message.channel.send("{} just bought {} for {} {}!".format(user.mention, bought_item["name"], bought_item["price"], shop.find_shop_by_id(reaction.message.id)["currency"]))
    elif user != client.user and reaction.emoji == "⭐":
        # For Quoting
        stats.increment_stat("quotes_submitted", 1)
        if reaction.message.id in already_quoted:
            return
        already_quoted.append(reaction.message.id)
        botspam_channel = client.get_channel(int(config.bot_spam))
        quote_channel = client.get_channel(int(config.quotes))
        request_embed = discord.Embed(title="Quote Request [Pending]", description="Message from {} in <#{}> requested for quote by {}:".format(reaction.message.author.mention,reaction.message.channel.id,user.mention), color=0x0000ff)
        request_embed.add_field(name="Message Content", value="```" + reaction.message.content.replace('`', '`\u200B') + "```")
        request_embed.set_footer(text="React with ✅ to accept or ❎ to deny.")
        request = await botspam_channel.send(embed=request_embed)
        await request.add_reaction("✅")
        await request.add_reaction("❎")

        def check(reaction, user):
            return config.game_master in [y.id for y in user.roles] and reaction.message.id == request.id

        try:
            reaction_confirm, user = await client.wait_for('reaction_add', timeout=172800, check=check)
        except asyncio.TimeoutError:
            request_embed = discord.Embed(title="Quote Request [Timed Out]", description="Message from {} in <#{}> requested for quote by {}:".format(reaction.message.author.mention,reaction.message.channel.id,user.mention), color=0xff0000)
            request_embed.add_field(name="Message Content", value="```" + reaction.message.content.replace('`', '`\u200B') + "```")
            await request.edit(embed=request_embed)
            await reaction_confirm.message.clear_reactions()
        else:
            if reaction_confirm.emoji == "✅":
                request_embed = discord.Embed(title="Quote Request [Approved By {}]".format(user), description="Message from {} in <#{}> requested for quote by {}:".format(reaction.message.author.mention,reaction.message.channel.id,user.mention), color=0x00ff00)
                request_embed.add_field(name="Message Content", value="```" + reaction.message.content.replace('`', '`\u200B') + "```")
                await request.edit(embed=request_embed)
                await reaction_confirm.message.clear_reactions()
                quote_embed = discord.Embed(description=reaction.message.content, color=0x0000ff)
                quote_embed.set_author(name=str(reaction.message.author), icon_url=reaction.message.author.avatar_url)
                quote_embed.set_footer(text="{} | {} (UTC)".format(reaction.message.guild.name, reaction.message.created_at.strftime('%d %B %H:%M:%S')))
                await quote_channel.send(embed=quote_embed)
            if reaction_confirm.emoji == "❎":
                stats.increment_stat("quotes_denied", 1)
                request_embed = discord.Embed(title="Quote Request [Denied By {}]".format(user), description="Message from {} in <#{}> requested for quote by {}:".format(reaction.message.author.mention,reaction.message.channel.id,user.mention), color=0xff0000)
                request_embed.add_field(name="Message Content", value="```" + reaction.message.content.replace('`', '`\u200B') + "```")
                await request.edit(embed=request_embed)
                await reaction_confirm.message.clear_reactions()


# Whenever a message is edited
@client.event
async def on_message_edit(before, after):
    if before.author == client.user: # We don't want to respond to our own edits
        return
    if before.content == after.content: # Ensure it wasn't just a pin
        return

    if before.id != after.id:
        db.add_trash_message(after.id,after.channel.id)

    #check role of sender
    isGameMaster = False
    isAdmin = False
    isPeasant = False
    try:
        if after.guild == client.get_channel(int(config.game_log)).guild:
            role_table = [y.id for y in after.guild.get_member(after.author.id).roles]

            if game_master in role_table:
                isGameMaster = True
            if administrator in role_table:
                isAdmin = True
            if peasant in role_table and after.author.bot == True:
                isPeasant = True
    except Exception:
        pass

    await process_message(after,process(after,isGameMaster,isAdmin,isPeasant))

# Whenever a message is sent.
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        #stats.increment_stat("bot_messages_sent", 1)
        return

    if random.randint(0,249) == 1:
        token = create_token(message.author.id)
        msg = await message.author.send("Hey, so... this doesn\'t work well yet - but give this code to the Game Masters for a small reward! *(If it works.)* ```" + token + "```")
        box.add_token(token,message.author.id,msg)
        await message.add_reaction('🎁')

    #check role of sender
    isGameMaster = False
    isAdmin = False
    isPeasant = False
    if message.guild == client.get_channel(int(config.game_log)).guild:
        try:
            role_table = [y.id for y in message.guild.get_member(message.author.id).roles]
        except Exception:
            print('Unable to acquire role_table from {}'.format(message.author.display_name))
        else:
            if game_master in role_table:
                isGameMaster = True
            if administrator in role_table:
                isAdmin = True
            if peasant in role_table and message.author.bot == True:
                isPeasant = True

    await process_message(message,process(message,isGameMaster,isAdmin,isPeasant))

async def process_message(message,result):
    general.add_activity(message.author.id,message.author.name)

    gamelog_channel = client.get_channel(int(config.game_log))
    botspam_channel = client.get_channel(int(config.bot_spam))
    storytime_channel = client.get_channel(int(config.story_time))

    # The temp_msg list is for keeping track of temporary messages for deletion.
    temp_msg = []

    for mailbox in result:

        # If a Mailbox says so, all existing polls will be evaluated.
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

                log, result, chosen_emoji = count_votes(user_table,poll.purpose,dy.get_mayor())

                await gamelog_channel.send(log)
                await poll_channel.send(result)

                chosen_one = db.emoji_to_player(chosen_emoji)
                chosen_one = int(chosen_one)

                if chosen_emoji != '' and chosen_one != None:
                    if poll.purpose == 'lynch':
                        db.add_kill(chosen_one,'Innocent')
                    elif poll.purpose == 'Mayor':
                        dy.set_mayor(chosen_one)
                        # TODO: give Mayor role
                    elif poll.purpose == 'Reporter':
                        dy.set_reporter(chosen_one)
                        # TODO: give Reporter role
                    elif poll.purpose == 'wolf':
                        db.add_kill(chosen_one,'Werewolf',db.random_wolf())
                    elif poll.purpose == 'cult':
                        db.add_kill(chosen_one,'Cult Leader',db.random_cult())
                    elif poll.purpose == 'thing':
                        db.add_kill(chosen_one,'The Thing','')

        for user_id in mailbox.demotions:
            if user_id == message.author.id and message.guild == gamelog_channel.guild:
                member = message.author
            else:
                member = gamelog_channel.guild.get_member(int(user_id))

            if member != None:
                for role in member.roles:
                    if role.id == config.mayor:
                        await member.remove_roles(role, reason="Demoting the Mayor")
                    if role.id == config.reporter:
                        await member.remove_roles(role, reason="Demoting the Reporter")

        # Create a new shop instance
        for element in mailbox.shops:
            shop_data = db_shop.get_shop_config(element.shop_config)
            i = 1
            j = 0
            emoji_table = []
            page_amount = int(len(shop_data["items"])-1/20)+1


            for item in shop_data["items"]:
                if j % 20 == 0:
                    embed = discord.Embed(title="Shop (Page {}/{})".format(i,page_amount), description=shop_data["shop_description"], color=0x00ff00)

                embed.add_field(name="[{}] {}".format(item["emoji"], item["name"]), value="{} {}\n*{}*\n".format(item["price"], shop_data["currency"], item["description"]), inline=False) # Add item to shop
                emoji_table.append(emojize(item["emoji"]))
                j += 1

                if j % 20 == 0:
                    i += 1
                    response = await client.get_channel(int(element.destination)).send(embed=embed)
                    db_shop.add_shop(response.id)

                    for item in emoji_table:
                        await response.add_reaction(item)
                    emoji_table = []

            if j % 20 != 0:
                response = await client.get_channel(int(element.destination)).send(embed=embed)
                db_shop.add_shop(response.id)

                for item in emoji_table:
                    await response.add_reaction(item)

        # If the Mailbox has a message for the gamelog, this is where it's sent.
        for element in mailbox.gamelog:
            msg = await gamelog_channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        # If the Mailbox has a message for the botspam, this is where it's sent.
        for element in mailbox.botspam:
            msg = await botspam_channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        # If the Mailbox has a message for the storytime (in-game announcements) channel, this is where it's sent.
        for element in mailbox.storytime:
            msg = await storytime_channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        # The messages are sent here if they are a direct message to the one sending a command.
        for element in mailbox.answer:
            msg = await message.channel.send(element.content)
            for emoji in element.reactions:
                await msg.add_reaction(emoji)
            if element.temporary == True:
                temp_msg.append(msg)

        # The messages that are destined for a specific channel, are sent here.
        for element in mailbox.channel:

            # The following code is sent if the message is an embed.
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
            # The following code is sent if the message is a regular message.
            else:
                msg = await client.get_channel(int(element.destination)).send(element.content)
                for emoji in element.reactions:
                    await msg.add_reaction(emoji)
                if element.temporary == True:
                    temp_msg.append(msg)

        # DMs are sent here.
        for element in mailbox.player:
            member = client.get_user(int(element.destination))
            main_guild = botspam_channel.guild
            if member == None:
                member = main_guild.get_member(int(element.destination))
            if member == None:
                await message.channel.send("Couldn't send a DM to <@{}>!".format(element.destination))
                await botspam_channel.send(
                    "<@{}> has attempted to send a DM to <@{}>, but failed, because we couldn't find the specified user via `client.get_user`.".format(
                        message.author.id, element.destination))
            else:
                try:
                    msg = await member.send(element.content)
                    for emoji in element.reactions:
                        await msg.add_reaction(emoji)
                    if element.temporary == True:
                        temp_msg.append(msg)
                except discord.errors.Forbidden:
                    botspam_channel.send('I wasn\'t allowed to send a DM to <@{}>! Here\'s the content:'.format(member.id))
                    botspam_channel.send(element.content)
                except Exception:
                    botspam_channel.send('I failed to send a DM to <@{}>! Could somebody send this, please?'.format(member.id))
                    botspam_channel.send(element.content)

        # Settings of existing channels are altered here.
        for element in mailbox.oldchannels:
            # element.channel - channel to be edited;
            # element.victim - person's permission to be changed;
            # element.number - type of setting to set to: see issue #83 for more info.

            channel = client.get_channel(element.channel)
            user = client.get_user(int(element.victim))
            main_guild = botspam_channel.guild
            member = main_guild.get_member(int(element.victim))
            if member == None:
                if user == None:
                    await botspam_channel.send("That\'s problematic! I couldn\'t edit the cc info of <@{0}> *(<#{0}> <@&{0}> ?)*".format(element.victim))
                    print('Unable to locate member {}.'.format(element.victim))
                member = user
            if channel == None:
                await botspam_channel.send('Unable to edit channel <#{0}> *(<@{0}> <@&{0}> ?)*'.format(int(element.victim)))
            elif member != None:
                await remove_all_game_roles(member)
                if element.number == 0:
                    await channel.set_permissions(user, read_messages=False, send_messages=False)
                    try:
                        if int(db_get(member.id,'frozen')) == 0:
                            raise NotImplementedError("This is a purposeful error raise!")
                    except Exception:
                        if db.isParticipant(member.id):
                            await member.add_roles(get_role(main_guild.roles, config.participant), reason="Updating CC Permissions")
                        elif db.isParticipant(member.id,True,True):
                            await member.add_roles(get_role(main_guild.roles, config.dead_participant), reason="Updating CC Permissions")
                        elif db.isParticipant(member.id,True,True,True):
                            await member.add_roles(get_role(main_guild.roles, config.suspended), reason="Updating CC Permissions")
                    else:
                        await member.add_roles(get_role(main_guild.roles, config.frozen_participant), reason="Updating CC Permissions")
                elif element.number == 1:
                    await channel.set_permissions(user, read_messages=True, send_messages=True)
                    await member.add_roles(get_role(main_guild.roles, config.participant), reason="Updating CC Permissions")
                elif element.number == 2:
                    await channel.set_permissions(user, read_messages=True, send_messages=False)
                    await member.add_roles(get_role(main_guild.roles, config.frozen_participant), reason="Updating CC Permissions")
                elif element.number == 3:
                    await channel.set_permissions(user, read_messages=False, send_messages=False)
                    await member.add_roles(get_role(main_guild.roles, config.participant), reason="Updating CC Permissions")
                elif element.number == 4:
                    await channel.set_permissions(user, read_messages=True, send_messages=False)
                    if db.isParticipant(member.id,False,True):
                        await member.add_roles(get_role(main_guild.roles, config.dead_participant), reason="Updating CC Permissions")
                elif element.number == 5:
                    await channel.set_permissions(user, read_messages=True, send_messages=False)
                    await member.add_roles(get_role(main_guild.roles, config.participant), reason="Updating CC Permissions")
                elif element.number == 6:
                    await channel.set_permissions(user, read_messages=False, send_messages=False)
                    await member.add_roles(get_role(main_guild.roles, config.participant), reason="Updating CC Permissions")
                elif element.number == 7:
                    await channel.set_permissions(user, read_messages=False, send_messages=False)
                    await member.add_roles(get_role(main_guild.roles, config.participant), reason="Updating CC Permissions")
                elif element.number == 8:
                    await channel.set_permissions(user, read_messages=False, send_messages=False)
                    await member.add_roles(get_role(main_guild.roles, config.suspended), reason="Updating CC Permissions")
                else:
                    await msg.channel.send('Something went wrong! Please contact a Game Master.')
                    return
                if db.isParticipant(element.victim,True,True):
                    db.set_user_in_channel(element.channel,element.victim,element.number)


        # New channels are created here.
        for element in mailbox.newchannels:
            # element.name - name of the channel;
            # element.owner - owner of the channel;
            # element.members - members of the channel
            # element.settlers - members for whom this shall become their home channel
            # element.secret - boolean if the channel is a secret channel

            if element.secret:
                element.owner = client.user.id

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

                # Add dead people & spectators to cc
                if not element.secret:
                    for user in [dead_buddy for dead_buddy in db.player_list() if dead_buddy not in db.player_list(True)]:
                        element.members.append(user)

                # Categorize all players
                for user in element.members:
                    member = main_guild.get_member(user)

                    if member == None:
                        await botspam_channel.send("That\'s problematic! I couldn\'t add <@{0}> to a cc. *(<#{0}> <@&{0}> ?)*".format(element.victim))
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
                    elif db_get(user,'role') == 'Suspended':
                        pass
                    else:
                        deadies.append(member)

                # Delete any potential duplicates
                viewers = list(set(viewers))
                frozones = list(set(frozones))
                abductees = list(set(abductees))
                deadies = list(set(deadies))

                # Role objects (based on ID)
                roles = main_guild.roles # Roles from the guild
                game_master_role = discord.utils.find(lambda r: r.id == game_master, roles)
                # TODO: Add read permissions for spectators if element.secret == False
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

                if not element.secret:
                    intro_msg = creation_messages.cc_intro([v.id for v in viewers])
                    reason_msg = 'CC requested by ' + message.author.name
                    title = "s{}_cc_{}".format(config.season,element.name)
                    category_name = 'S{} CCs PART {}'.format(config.season,db.count_categories(element.secret) + 1)
                else:
                    intro_msg = secret_messages.creation(element.name,[v.id for v in viewers])
                    reason_msg = 'Secret {} channel created.'.format(element.name)
                    title = "s{}_{}".format(config.season,element.name)
                    category_name = 'S{} Secret Channels Part {}'.format(config.season,db.count_categories(element.secret) + 1)

                # Create a new category if needed
                if db.get_category(element.secret) == None:
                    category = await main_guild.create_category(category_name, reason='It seems like we couldn\'t use our previous category! Don\'t worry, I just created a new one.')
                    db.add_category(category.id,element.secret)
                else:
                    category = main_guild.get_channel(db.get_category(element.secret))

                try:
                    # Create the text channel
                    channel = await main_guild.create_text_channel(
                        name=title,
                        category=category,
                        overwrites=default_permissions,
                        reason=reason_msg)
                    db.add_channel(channel.id,element.owner,element.secret)
                    if element.secret:
                        db.add_secret_channel(channel.id,element.name)

                        # If the channel is meant for an amulet holder, assign the amulet holder.
                        if element.name == 'Amulet_Holder':
                            for member in viewers:
                                if db_get(member.id,'role') == 'Amulet Holder':
                                    db_set(member.id,'amulet',channel.id)
                    if element.trashy:
                        db.add_trash_channel(channel.id)

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


        # Polls are created here.
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
                        msg = await client.get_channel(int(element.channel)).send(msg)
                        for emoji in emoji_table:
                            await msg.add_reaction(emoji)
                        msg_table.append(msg)
                        emoji_table = []
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


        # Categories are deleted here.
        for element in mailbox.deletecategories:
            id = element.channel
            category = client.get_channel(id)
            if category != None:
                bot_message = await message.channel.send('Please react with 👍 to confirm deletion of category `' + category.name + '`.\n\nNote: This action will irreversibly delete all channels contained within the specified category. Please use with discretion.')
                await bot_message.add_reaction('👍')
                def check(reaction, user):
                    return user == message.author and str(reaction.emoji) == '👍'
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await message.channel.send('Confirmation timed out.')
                    try:
                        await bot_message.delete()
                    except Exception:
                        pass
                else:
                    await message.channel.send('Ok, I\'ll get right on that.\n\n*This might take some time.*')
                    for channel in category.channels:
                        await channel.delete()
                    await category.delete()
                    await message.channel.send('\n:thumbsup: Channels and category deleted')
            else:
                await message.channel.send('Sorry, I couldn\'t find that category.')

        clean_time = len(mailbox.cleaners)
        if clean_time > 0:
            await botspam_channel.send("Cleaning up {} channels! This may take some time.".format(clean_time))

        for channel in mailbox.cleaners:

            trash_channel = client.get_channel(int(channel))

            if trash_channel != None:
                for message_id in db.empty_trash_channel(channel):
                    message = await trash_channel.get_message(int(message_id))
                    if message != None:
                        await message.delete()

    # Delete all temporary messages after about two minutes.
    await asyncio.sleep(120)
    for msg in temp_msg:
        try:
            await msg.delete()
        except Exception:
            # Unable to delete the message.
            # It was probaly already deleted or something.
            pass


# Whenever the bot regains his connection with the Discord API.
@client.event
async def on_ready():
    print(' --> Logged in as')
    print('   | > ' + client.user.name)
    print('   | > ' + str(client.user.id))

    await client.get_channel(welcome_channel).send('Beep *booooo.....*p! I just went online!')

print(splash)
print(' --> "' + random.choice(splashes) + '"')
print(' --> Please wait whilst we connect to the Discord API...')
try:
    client.run(config.GH_TOKEN)
except:
    print('   | > Error logging in. Check your token is valid and you are connected to the Internet.')

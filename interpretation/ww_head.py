# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from discord import Embed

import interpretation.check as check
import roles_n_rules.functions as func
from config import max_cc_per_user, season, universal_prefix as unip, max_participants
from config import ww_prefix as prefix
from interpretation.check import is_command
from main_classes import Mailbox
from management.position import valid_distribution
from management.db import isParticipant, personal_channel, db_get, db_set, signup, emoji_to_player, channel_get, \
    is_owner, get_channel_members
from story_time.commands import cc_goodbye, cc_welcome
from roles_n_rules.role_data import attack
from communication.emoji import random_emoji
import story_time.eastereggs as eggs
import roles_n_rules.switch as switch
from management import db, dynamic as dy
import management.setup as setup

PERMISSION_MSG = "Sorry, but you can't run that command! You need to have **{}** permissions to do that."
def todo():
    return [Mailbox().respond("I am terribly sorry! This command doesn't exist yet!", True)]


def process(message, isGameMaster=False, isAdmin=False, isPeasant=False):
    user_id = message.author.id
    message_channel = message.channel.id
    user_role = db_get(user_id, 'role')

    help_msg = "**List of commands:**\n"

#    '''day'''
#    if is_command(message, ['day']):
#        return [switch.day(),Mailbox().respond("Dayyyyyy")]
#
#    '''standoff'''
#    if is_command(message,['stand']):
#        users = check.users(message,2,True)
#        role = check.roles(message)
#        if not users or not role:
#            return [Mailbox().respond("**NO**")]
#        db.add_standoff(users[0],role[0],users[1])
#        return [Mailbox().respond("<@{}> snipes <@{}> as {}. Gotcha.".format(users[1],users[0],role[0]))]
#
#    '''tokill'''
#    if is_command(message,['tokill']):
#        users = check.users(message,2,True)
#        role = check.roles(message)
#        if not users or not role:
#            return [Mailbox().respond("**NO**")]
#        db.add_kill(users[0],role[0],users[1])
#        return [Mailbox().respond("<@{}> kills <@{}> as {}. Gotcha.".format(users[1],users[0],role[0]))]
#
#    '''evaluate'''
#    if is_command(message, ['eval']):
#        return [Mailbox(True)]
#
#    '''testpoll'''
#    if is_command(message,['poll','testpoll']):
#        return [Mailbox().new_poll(message.channel.id,'wolf',message.author.id,message.content.split(' ',1)[1])]
#
#    '''dist'''
#    if is_command(message,['dist','checkdist','check_dist']):
#        roles = check.roles(message)
#        if not roles:
#            return [Mailbox().respond("You gotta provide some roles, bud!",True)]
#        judgment = valid_distribution(roles)
#        if not judgment:
#            return [Mailbox().respond("Sorry, that's an invalid role distribution!",True)]
#        return [Mailbox().respond(judgment,True)]

    # =============================================================
    #
    #                         BOT COMMANDS
    #
    # =============================================================
    if isPeasant == True:
        if is_command(message,['warn'],False,unip):
            # Warn the user that they've been inactive for a while.
            answer = Mailbox().story("Hey there, <@{}>! You have been idling for about 48 hours now!\n".format(message.mentions[0].id))
            return [answer.story_add("Please let us hear from you within 24 hours, or you will be disqualified for idling out.")]

        if is_command(message,['idle'],False,unip):
            # Kill the inactive user
            answer = Mailbox().story("<@{}> has been killed due to inactivity.".format(message.mentions[0].id))
            return [attack(message.mentions[0].id,'Inactive','',answer.log(""))]

        if is_command(message,['pay'],False,unip):
            # Initiate the day.
            return switch.pay()

        if is_command(message,['day'],False,unip):
            # Initiate the second part of the day
            return [switch.day()]

        if is_command(message,['pight'],False,unip):
            # Initiate the night.
            return switch.pight()

        if is_command(message,['night'],False,unip):
            # Initiate the second part of the night.
            return [switch.night()]

    # =============================================================
    #
    #                         ADMINISTRATOR
    #
    # =============================================================
    if isAdmin == True:
        help_msg += "\n __Admin commands:__\n"

        '''delete_category'''
        # This command is used to entirely delete a category and all channels in it
        # (Note that this will A: take a while due to ratelimits and B: Spam the audit log)
        # Moderation should be used to ensure this command is not used outside of where it's allowed
        if is_command(message, ['delete_category']):
            int_table = check.numbers(message)
            if int_table == False:
                return [Mailbox().respond(
                    "**Invalid syntax:** Missing category id.\n\n`" + prefix + "delete_category <category id>`")]
            answer = Mailbox()
            for id in int_table:
                answer.delete_category(id)
            return [answer]
        if is_command(message, ['delete_category'], True):
            msg = "**Usage:** Deletes an entire category and all channels in it.\n\n`" + prefix + "delete_category <id>`\n\n**Example:** `" + prefix + "delete_category 457264810363584513`"
            msg += "\nThe command does not accept multiple categories. This command can only be used by Game Masters."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "delete_category` - Delete a category.\n"

        '''start'''
        # This command is used to start a game.
        if is_command(message, ['start']):
            return [switch.start_game()]
        if is_command(message, ['start'], True):
            return [Mailbox().respond("**Usage:** Start the game.\n\n`" + prefix + "start`\n\nThis command can only be used by Administrators.")]
    elif is_command(message, ['delete_category','start']):
        return [Mailbox().respond(PERMISSION_MSG.format("Administrator"), True)]


    # =============================================================
    #
    #                         GAME MASTERS
    #
    # =============================================================
    if isGameMaster == True:
        help_msg += "\n__Game Master commands:__\n"

        '''addrole'''
        # Before the game starts, a list of roles is kept track of.
        # That list is the list of roles that will be dealt among the participants.
        # If the list is greater than the amount of participants, some random roles will be left out.
        # The game cannot start as long as this list is incomplete.
        if is_command(message, ['addrole']):
            amount = check.numbers(message)
            if not amount:
                amount = [1]
            role = check.roles(message)
            if not role:
                return [Mailbox().respond("**INVALID SYNTAX:** No role provided.\n\nPlease give us a role to add.")]
            setup.add_role(role[0],amount[0])
            return [Mailbox().respond("You have successfully added the **{}** role {} times to the game pool!".format(role[0],amount[0]))]
        if is_command(message, ['addrole'], True):
            msg = "**Usage:** Add a role to the game pool\n\n`" + prefix + "addrole <role>`\n\n**Example:** `" + prefix + "addrole Innocent`"
            msg += "\nThe command accepts multiple roles. This command can only be used by Game Masters."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "addrole` - Add role to game pool.\n"

        '''assign'''
        # This command is used at the start of the game to assign all roles.
        # This will actually set their "fakerole" value, which will be transferred to their actual role once the game starts.
        if is_command(message, ['assign']):
            role = check.roles(message, 1)
            user = check.users(message, 1)

            if role == False:
                return [Mailbox().respond("No role provided! Please provide us with a role!")]
            if user == False:
                return [Mailbox().respond("No user found! Please provide us with a user!")]
            if isParticipant(user[0], True, True) == False:
                return [Mailbox().respond(
                    "I am terribly sorry. You cannot assign a role to a user that hasn\'t signed up!")]

            db_set(user[0], 'role', role[0])
            return [Mailbox().spam("You have successfully given <@{}> the role of the `{}`!".format(user[0], role[0]))]

        if is_command(message, ['assign'], True):
            msg = "**Usage:** Give a player a specific role\n\n`" + prefix + "assign <user> <role>`\n\nExample: `" + prefix
            msg += "assign @Randium#6521 Innocent`\nThis command can only be used by Game Masters."
            return [Mailbox().spam(msg)]
        help_msg += "`" + prefix + "assign` - Give player a given role.\n"

        '''day'''
        # This command is used to initialize the day.
        if is_command(message, ['day']):
            # TODO
            return todo()
        if is_command(message, ['day'], True):
            msg = "**Usage:** Initiate the day if this does not happen automatically.\n\n"
            msg += "`" + prefix + "day`\n\nThis command can only be used by Game Masters."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "day` - Force the day to start.\n"

        '''donate'''
        # This command allows the Game Masters to give more active users a few extra conspiracy channels if they need them.
        # It will not be used very often in practice, but it'll get the active players relaxed.
        # They all start hysterically panicking when you start talking about finite amounts.
        if is_command(message,['donate','give_cc','more_cc']):
            target = check.users(message,1,True,True)
            if not target:
                return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
            number = check.numbers(message,1)
            if not number:
                return [Mailbox().respond("**INVALID SYNTAX:**\nNo number provided.",True)]

            ccs_owned = int(db_get(target[0],'ccs'))
            db_set(target[0],'ccs',ccs_owned-number[0])
            return [Mailbox().spam("<@{}> has received {} extra conspiracy channel slots.".format(target[0],number[0]))]
        if is_command(message,['donate','give_cc','more_cc'],True):
            return [Mailbox().respond("**Usage:** Give a player more cc's.\n\n`" + prefix + "donate <user> <number>`\n\n**Example:** `" + prefix + "donate @Randium#6521 3`",True)]
        help_msg += "`" + prefix + "donate` - Give a player more cc's.\n"

        '''info'''
        # This command allows users to view information about a conspiracy channel.
        # Says the user must be in a cc if they're not.
        if is_command(message, ['info']):
            guild = message.channel.guild
            try:
                owner_id = channel_get(message.channel.id, 'owner')
            except:
                return [Mailbox().respond(
                    'Sorry, but it doesn\'t look like you\'re in a CC! If you are, please alert a Game Master as soon as possible.')]
            if owner_id != None:
                owner_object = guild.get_member(int(owner_id))
            else:
                owner_object = None
            embed = Embed(color=0x00cdcd, title='Conspiracy Channel Info')
            if owner_object != None and owner_id != None:
                embed.add_field(name='Channel Owner', value='<@' + owner_id + '>')
                embed.set_thumbnail(url=owner_object.avatar_url)
            elif owner_id == None:
                return [Mailbox().respond(
                    'Sorry, but it doesn\'t look like you\'re in a CC! If you are, please alert a Game Master as soon as possible.')]
            else:
                try:
                    owner_name = db_get(owner_id, 'name')
                    if str(owner_name) == 'None':
                        owner_name = 'Sorry, an error was encountered. Please alert a Game Master.'
                except:
                    owner_name == 'Sorry, an error was encountered. Please alert a Game Master.'

                embed.add_field(name='Channel Owner', value=owner_name)
            member_text = ""
            for member in get_channel_members(message.channel.id):
                member_text += "<@" + str(member) + "> "
            # Parse channel name
            channel_display = ''
            for letter in message.channel.name:
                if letter == '_':
                    channel_display += '\\'
                channel_display += letter
            embed.add_field(name='Channel Name', value=channel_display[3+len(season):])
            embed.add_field(name='Participants', value=member_text)
            embed.set_footer(text='Conspiracy Channel Information requested by ' + message.author.nick)
            return [Mailbox().embed(embed, message.channel.id)]
        if is_command(message, ['info'], True):
            msg = "**Usage:** Gain information about a conspiracy channel.\n\n`" + prefix + "info`\n\n"
            msg += "Try it! You\'ll see what it does."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "info` - Gain info about conspiracy channel.\n"

        '''night'''
        # This command is used to initialize the day.
        if is_command(message, ['night']):
            # TODO
            return todo()
        if is_command(message, ['night'], True):
            msg = "**Usage:** Initiate the night if this does not happen automatically.\n\n"
            msg += "`" + prefix + "night`\n\nThis command can only be used by Game Masters."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "night` - Force the night to start.\n"

        '''open_signup'''
        # This command is started when a new game can be started.
        # Make sure the bot has reset itself beforehand.
        if is_command(message, ['open_signup']):
            if dy.get_signup() == 0:
                dy.set_signup(1)
                answer = Mailbox().story("Alright, @everyone! Who's excited for a new game? I am.\n")
                answer.story_add("This time, up to {} players can sign up. Be quick!".format(max_participants))
                return [answer.spam('<@{}> has opened the signups.'.format(user_id))]
            if dy.get_signup() == 1:
                return [Mailbox().respond('Don\'t worry, bud! The signups are already open.')]
            if dy.get_signup() == 2:
                return [Mailbox().respond('I\'m sorry, but you can\'t open sign ups if there\'s already a game going.')]
        if is_command(message, ['open_signup'], True):
            msg = "**Usage:** Allow users to sign up for a new game.\n\n`" + prefix + "open_signup`\n\n"
            msg += "This command can only be used by Game Masters."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "open_signup` - Allow users to sign up.\n"

        '''whois'''
        # This command reveals the role of a player.
        # To prevent spoilers, the response isn't made in the message's channel, but rather in the bot spam channel.
        if is_command(message, ['whois']):
            user_table = check.users(message)
            identities = Mailbox()

            if user_table == False:
                return [Mailbox().respond("**ERROR:** No user provided!", True)]

            for user in user_table:
                emoji = db_get(user, 'emoji')
                role = db_get(user, 'role')
                member = message.channel.guild.get_member(int(user))
                if emoji == None or role == None:
                    identities.spam("**ERROR:** Could not find user <@{}> in database.".format(user))
                elif member == None:
                    identities.spam(
                        "I am sorry, but I couldn\'t find <@{}> on this server! Try again, please!".format(user))
                else:
                    special_tags = ""
                    if int(db_get(user, 'abducted')) == 1:
                        special_tags += '[Abducted] '
                    if int(db_get(user, 'bites')) > 0:
                        special_tags += '[Bitten] '
                    if int(db_get(user, 'demonized')) == 1:
                        special_tags += '[Demonized] '
                    if db_get(user, 'fakerole') != role:
                        special_tags += "[Disguised as {}] ".format(db_get(user, 'fakerole'))
                    if int(db_get(user, 'enchanted')) == 1:
                        special_tags += "[Enchanted] "
                    if int(db_get(user, 'frozen')) == 1:
                        special_tags += '[Frozen] '
                    if int(db_get(user, 'powdered')) == 1:
                        special_tags += '[Powdered] '
                    if int(db_get(user, 'souls')) > -1:
                        special_tags += '[Soulless One] '
                    if int(db_get(user, 'threatened')) > 0:
                        special_tags += "[Threatened] "
                    if int(db_get(user, 'undead')) == 1:
                        special_tags += '[Undead] '
                    if int(db_get(user, 'votes')) == 0:
                        special_tags += '[Silenced] '
                    if special_tags == "":
                        special_tags += "None"
                    embed = Embed(color=0xcd9e00, title='User Info')
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.add_field(name="Name", value="<@{}>".format(user))
                    embed.add_field(name="Emoji", value=emoji)
                    embed.add_field(name="Role", value=role)
                    embed.add_field(name="Attributes", value=special_tags)
                    embed.set_footer(text='Participant Information requested by ' + message.author.name)
                    identities.embed(embed, 'spam')

            return [identities]

        if is_command(message, ['whois'], True):
            msg = "**Usage:** Gain all the wanted info about a player.\n\n`" + prefix + "whois <user1> <user2> ...`\n\n"
            msg += "**Example:** `" + prefix + "whois @Randium#6521`\nThe command will only answer in the botspam-channel, "
            msg += "to prevent any accidental spoilers from occurring. This command can only be used by Game Masters."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "whois` - Gain a user's information\n"
    elif is_command(message, ['addrole','assign','day','night','open_signup','whois']):
        return [Mailbox().respond(PERMISSION_MSG.format("Game Master"), True)]

    # =============================================================
    #
    #                         PARTICIPANTS
    #
    # =============================================================

    if isParticipant(user_id):
        help_msg += "\n__Participant commands:__\n"

        user_undead = int(db_get(user_id,'undead'))

        '''add'''
        # This command allows users to add users to a conspiracy.
        # This command will not trigger if the user doesn't own the conspiracy channel.
        if is_command(message, ['add']):
            members_to_add = check.users(message)
            if members_to_add == False:
                return [Mailbox().respond("I am sorry! I couldn't find the user you were looking for!", True)]
            if is_owner(user_id, message_channel) == False:
                return [Mailbox().respond(
                    "I\'m sorry, you can only use this in conspiracy channels where you are the owner!")]

            command = Mailbox()
            for member in members_to_add:
                if isParticipant(member) == False:
                    command.edit_cc(message_channel, member, 4)
                elif int(db_get(member, 'abducted')) == 1:
                    command.edit_cc(message_channel, member, 3)
                elif int(db_get(member, 'frozen')) == 1:
                    command.edit_cc(message_channel, member, 2)
                else:
                    command.edit_cc(message_channel, member, 1)
            return [command.respond(cc_welcome(member))]

        if is_command(message, ['add'], True):
            msg = "**Usage:** Add a user to the existing conspiracy channel.\n\n`" + prefix + "add <user>`\n\n"
            msg += "**Example:** `" + prefix + "add @Randium#6521`\nThis command can only be used by the owner of "
            msg += "the conspiracy channel. To see who owns a given conspiracy channel, type `" + prefix + "info`."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "add` - Add player to conspiracy channel.\n"

        '''cc'''
        # This command allows users to create a conspiracy channel.
        if is_command(message, ['cc']):
            if len(message.content.split(' ')) < 2:
                return [Mailbox().respond(
                    "**Invalid syntax:**\n\n`" + prefix + "cc <name> <user1> <user2> <user3> ...`\n\n**Example:** `" + prefix + "cc the_cool_guys @Randium#6521`")]

            channel_members = check.users(message)
            if channel_members == False:
                channel_members = []
            if user_id not in channel_members:
                channel_members.append(user_id)

            num_cc_owned = int(db_get(user_id, 'ccs'))

            if num_cc_owned >= max_cc_per_user:
                answer = Mailbox().dm("You have reached the amount of conspiracy channels one may own!", user_id)
                return [answer.dm(
                    "If you want more conspiracy channels, please request permission from one of the Game Masters.",
                    user_id)]

            db_set(user_id, 'ccs', num_cc_owned + 1)
            answer = Mailbox().create_cc(message.content.split(' ')[1], user_id, channel_members)
            answer.spam("<@{}> has created a *conspiracy channel* called {}!".format(user_id, message.content.split(' ')[1]))
            if num_cc_owned + 1 >= max_cc_per_user:
                answer.spam("**Warning:** <@{}> has reached the maximum amount of conspiracy channels!\n".format(user_id))
                answer.spam_add("Use `" + prefix + "donate` to give them more channels to create!")
            return [answer]

        if is_command(message, ['cc'], True):
            msg = "**Usage:** create a *conspiracy channel*, a private channel where one can talk with a selected group of players.\n\n"
            msg += "`" + prefix + "cc <name> <user1> <user2> <user3> ...`\n\n**Example:** `" + prefix + "cc the_cool_guys @Randium#6521`\n"
            msg += "Please do not abuse this command to create empty channels without a purpose. Abuse will be noticed and dealt with accordingly."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "cc` - Create a new conspiracy channel.\n"

        '''info'''
        # This command allows users to view information about a conspiracy channel.
        # Says the user must be in a cc if they're not.
        if is_command(message, ['info']):
            guild = message.channel.guild
            try:
                owner_id = channel_get(message.channel.id, 'owner')
            except:
                return [Mailbox().respond(
                    'Sorry, but it doesn\'t look like you\'re in a CC! If you are, please alert a Game Master as soon as possible.')]
            if owner_id != None:
                owner_object = guild.get_member(int(owner_id))
            else:
                owner_object = None
            embed = Embed(color=0x00cdcd, title='Conspiracy Channel Info')
            if owner_object != None and owner_id != None:
                embed.add_field(name='Channel Owner', value='<@' + owner_id + '>')
                embed.set_thumbnail(url=owner_object.avatar_url)
            elif owner_id == None:
                return [Mailbox().respond(
                    'Sorry, but it doesn\'t look like you\'re in a CC! If you are, please alert a Game Master as soon as possible.')]
            else:
                try:
                    owner_name = db_get(owner_id, 'name')
                    if str(owner_name) == 'None':
                        owner_name = 'Sorry, an error was encountered. Please alert a Game Master.'
                except:
                    owner_name == 'Sorry, an error was encountered. Please alert a Game Master.'

                embed.add_field(name='Channel Owner', value=owner_name)
            member_text = ""
            for member in get_channel_members(message.channel.id):
                member_text += "<@" + str(member) + "> "
            # Parse channel name
            channel_display = ''
            for letter in message.channel.name:
                if letter == '_':
                    channel_display += '\\'
                channel_display += letter
            embed.add_field(name='Channel Name', value=channel_display[3+len(season):])
            embed.add_field(name='Participants', value=member_text)
            embed.set_footer(text='Conspiracy Channel Information requested by ' + message.author.display_name)
            return [Mailbox().embed(embed, message.channel.id)]
        if is_command(message, ['info'], True):
            msg = "**Usage:** Gain information about a conspiracy channel.\n\n`" + prefix + "info`\n\n"
            msg += "Try it! You\'ll see what it does."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "info` - Gain info about conspiracy channel.\n"

        '''myrole'''
        # This command sends the user's role back to them in a DM.
        if is_command(message, ['myrole']):
            if int(db_get(message.author.id, 'undead')) == 0:
                return [
                    Mailbox().dm("Your role is **{}**.".format(db_get(message.author.id, 'role')), message.author.id,
                                 False, [db_get(message.author.id, 'emoji')])]
            return [Mailbox().dm("You pretend to be a **{}**, while you are secretly an **Undead**!".format(
                db_get(message.author.id, 'role')), message.author.id)]
        if is_command(message, ['myrole'], True):
            msg = "**Usage:** Get a DM of what your role is.\n\n`" + prefix + "myrole`\n\n"
            msg += "This command may sound silly, but it could be useful if the player is confused about whether certain "
            msg += "scenarios have changed their role or not."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "myrole` - See your own role.\n"

        '''remove'''
        # This command removes a given user from a conspiracy channel.
        # A user should not get removed if they're the channel owner.
        if is_command(message, ['remove']):
            members_to_remove = check.users(message)
            if is_owner(user_id, message_channel) == False:
                return [Mailbox().respond("I\'m sorry, but you can only use this command in a cc that you own!")]
            command = Mailbox().respond("Looks like we\'ll have to say goodbye!")
            for member in members_to_remove:
                if is_owner(member, message_channel) == True:
                    command.respond(
                        "Sorry bud, ya can\'t remove the cc's owner! Blame the people who used to do this on purpose.")
                else:
                    command.edit_cc(message_channel, member, 0)
                    command.respond(cc_goodbye(member))
            return [command]

        if is_command(message, ['remove'], True):
            msg = "**Usage:** Remove a user from a conspiracy channel.\n\n`" + prefix + "remove <user>`\n\n"
            msg += "**Example:** `" + prefix + "remove @Randium#6521`\nThis command can only be used by the conspiracy channel owner."
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "remove` - Remove player from conspiracy channel.\n"

        # =======================================================
        #                ROLE SPECIFIC COMMANDS
        # =======================================================
        if personal_channel(user_id, message_channel) == True:
            help_msg += "\n"

            # This is going to have to be moved. This can't stay here.
            '''give_amulet'''
            # This command can be executed by everyone, but only in one channel.
            # That's the amulet channel.
            # To be worked out how exactly.
            if is_command(message, ['give_amulet']):
                # TODO
                return todo()
            if is_command(message, ['give_amulet'], True):
                # TODO
                return todo()
            help_msg += "`" + prefix + "give_amulet`\n"

            '''assassinate'''
            # Assassin's command; kill a victim
            if is_command(message, ['assassinate', 'kill']) and user_role == "Assassin":
                target = check.users(message, 1, True, True)
                if target == False:
                    return [Mailbox().respond(
                        "**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",
                        True)]
                return [func.nightly_kill(user_id, target[0])]
            if is_command(message,['assassinate','kill'],True) and user_role == "Assassin":
                msg = "**Usage:** Kill another player.\n\n`" + prefix + "kill <player>`\n\n"
                msg += "**Example:** `" + prefix + "kill @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by Assassins during the night."
                return [Mailbox().respond(msg,True)]
            if user_role == "Assassin" and user_undead == 0:
                help_msg += "`" + prefix + "kill` - Execute a player (Assassin only)\n"

            '''aura'''
            # The command for aura tellers
            if is_command(message,['aura','tell','vision']) and user_role == "Aura Teller":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.aura(user_id,target[0])]
            if is_command(message,['aura','tell','vision'],True) and user_role == "Aura Teller":
                msg = "**Usage:** View a player's aura.\n\nn`" + prefix + "aura <player>`\n\n"
                msg += "**Example:** `" + prefix + "aura @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by Aura Tellers during the night."
            if user_role == "Aura Teller" and user_undead == 0:
                help_msg += "`" + prefix + "aura` - View a player's aura (Aura Teller only)\n"

            '''barber_kill'''
            # Barber kill - to assassinate a victim during the day
            if is_command(message, ['assassinate', 'barber_kill', 'cut']) and user_role == "Barber":
                # TODO
                return todo()
            if is_command(message,['assassinate','barber_kill','cut'],True) and user_role == "Barber":
                msg = "**Usage:** Kill a player during the day.\n\n`" + prefix + "cut <player>`\n\n"
                msg += "**Example:** `" + prefix + "cut @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by barbers during the day. This command only works once, so choose wisely."
            if user_role == "Barber" and user_undead == 0:
                help_msg += "`" + prefix + "cut` - Execute a player (Barber only)\n"

            '''seek'''
            # Crowd seeker's power
            if is_command(message, ['crowd', 'seek']) and user_role == "Crowd Seeker":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                guessed_role = check.roles(message,1,True)
                if not guessed_role:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to name a role.")]
                return [func.seek(user_id,target[0],guessed_role[0])]
            if is_command(message,['crowd','seek'],True) and user_role == "Crowd Seeker":
                msg = "**Usage:** Inspect a player's role.\n\n`" + prefix + "seek <player> <role>`\n\n"
                msg += "**Example:** `" + prefix + "seek @Randium#621 Innocent`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by crowd seekers during the first night."
            if user_role == "Crowd Seeker" and user_undead == 0:
                help_msg += "`" + prefix + "seek` - Seek a player's role (Crowd Seeler only)\n"

            '''kiss'''
            # Cupid's power to fall in love with someone.
            if is_command(message, ['kiss', 'love', 'shoot']) and user_role == "Cupid":
                # TODO
                return todo()
            if is_command(message,['kiss','love','shoot'],True) and user_role == "Cupid":
                msg = "**Usage:** Fall in love with another player.\n\n`" + prefix + "love <player>`\n\n"
                msg += "**Example:** `" + prefix + "love @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by the cupid during the night."
            if user_role == "Cupid" and user_undead == 0:
        	    help_msg += "`" + prefix + "kiss` - Fall in love with a player. (Cupid only)\n"

            '''follow'''
            # The command that allows the dog to choose a side.
            if is_command(message, ['bark', 'become', 'choose', 'follow']) and user_role == "Dog":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                disguise = check.roles(message,1)
                if not disguise:
                    return [Mailbox().respond("**INVALID SYNTAX:** \nPlease make sure to provide a role.")]
                return [func.disguise(user_id,target[0],disguise[0])]
            if is_command(message,['bark','become','choose','follow'],True) and user_role == "Dog":
                msg = "**Usage:** Choose a role to play as.\n\n`" + prefix + "choose <role>`\n\n"
                msg += "**Example:** `" + prefix + "choose Innocent`\nThe options are **Innocent**, **Cursed Civilian** and **Werewolf**. "
                msg += "This command can only be used by the dog during the first night."
            if user_role == "Dog" and user_undead == 0:
                help_msg += "`" + prefix + "choose` - Choose a role to play as. (Dog only)\n"

            '''execute'''
            # This command allows the executioner to choose a replacement target.
            if is_command(message, ['choose', 'execute']) and user_role == "Executioner":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.executioner(user_id,target[0])]
            if is_command(message,['choose','execute'],True) and user_role == "Executioner":
                msg = "**Usage:** Choose a victim to die instead of you on the lynch.\n\n`" + prefix + "execute <player>`\n\n"
                msg += "**Example:** `" + prefix + "execute @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by executioners it can be used for an unlimited amount of times."
            if user_role == "Executioner" and user_undead == 0:
                help_msg += "`" + prefix + "exxecute` - Choose execution victim. (Executioner only)\n"

            '''undoom'''
            # The Exorcist's command.
            if is_command(message, ['exercise', 'exorcise', 'undoom']) and user_role == "Exorcist":
                # TODO
                return todo()
            if is_command(message,['exercise','exorcise','undoom'],True) and user_role == "Exorcist":
                msg = "**Usage:** Undoom a player.\n\n`" + prefix + "undoom <player>`\n\n"
                msg += "**Example:** `" + prefix + "undoom @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by ."
            if user_role == "Exorcist":
                help_msg += "`" + prefix + "undoom` - Undoom a player. (Exorcist only)\n"

            '''inspect'''
            # The fortune teller's command.
            if is_command(message, ['forsee', 'inspect', 'see', 'tell']) and user_role == "Fortune Teller":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.see(user_id,target[0])]
            if is_command(message, ['forsee', 'inspect', 'see', 'tell'], True) and user_role == "Fortune Teller":
                msg = "**Usage:** See a player's role.\n\n`" + prefix + "see <player>`\n\n"
                msg += "**Example:** `" + prefix + "see @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by fortune tellers."
                return [Mailbox().respond(msg,True)]
            if user_role == "Fortune Teller" and user_undead == 0:
                help_msg += "`" + prefix + "see` - Inspect a player's role (Fortune Teller only)\n"

            '''silence'''
            # Grandma's command.
            if is_command(message, ['knit', 'knot', 'silence']) and user_role == "Grandma":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.silence(user_id,target[0])]
            if is_command(message, ['knit', 'knot', 'silence'], True) and user_role == "Grandma":
                msg = "**Usage:** Make a user's vote invalid for the next day.\n\n`" + prefix + "silence <player>`\n\n"
                msg += "**Example:** `" + prefix + "silence @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by Grandma."
                return [Mailbox().respond(msg,True)]
            if user_role == "Grandma" and user_undead == 0:
                help_msg += "`" + prefix + "silence` - Silence a player. (Grandma only)\n"

            '''hook'''
            # The hooker's command
            if is_command(message, ['fuck', 'hook', 'sleep']) and user_role == "Hooker":
                # TODO
                return todo()
            if is_command(message, ['fuck', 'hook', 'sleep'], True) and user_role == "Hooker":
                msg = "**Usage:** Choose a player to sleep with.\n\n`" + prefix + "sleep <player>`\n\n"
                msg += "**Example:** `" + prefix + "sleep @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by Hookers."

                return [Mailbox().respond(msg,True)]
            if user_role == "Hooker" and user_undead == 0:
                help_msg += "`" + prefix + "hook` - Sleep with another player. (Hooker only)\n"

            '''hunt'''
            # The huntress' command. Used to keep track of whom will be shot.
            if is_command(message, ['hunt', 'shoot']) and user_role == "Huntress":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.executioner(user_id,target[0])]
            if is_command(message, ['hunt', 'shoot'], True) and user_role == "Huntress":
                msg = "**Usage:** Choose a player as a death target.\n\n`" + prefix + "hunt <player>`\n\n"
                msg += "**Example:** `" + prefix + "hunt @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by the Huntress."
                return [Mailbox().respond(msg,True)]
            if user_role == "Huntress" and user_undead == 0:
                help_msg += "`" + prefix + "hunt` - Choose player as death target. (Huntress only)\n"

            '''unfreeze'''
            # The innkeeper's command
            if is_command(message,['melt','unfreeze']) and user_role == "Innkeeper":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.unfreeze(user_id,target[0])]
            if is_command(message,['melt','unfreeze'],True) and user_role == "Innkeeper":
                msg = "**Usage:** Unfreeze a frozen player.\n\n`" + prefix + "melt <player>`\n\n"
                msg += "**Example:** `" + prefix + "melt @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by Innkeepers during the night."
            if user_role == "Innkeeper" and user_undead == 0:
                help_msg += "`" + prefix + "melt` - Unfreeze frozen player (Innkeeper only)\n"

            '''copy'''
            # The Look-Alike's command
            if is_command(message, ['copy', 'imitate', 'mirror', 'resemble']) and user_role == "Look-Alike":
                # TODO
                return todo()
            if is_command(message, ['copy', 'imitate', 'mirror', 'resemble'], True) and user_role == "Look-Alike":
                msg = "**Usage:** Copy a players role.\n\n`" + prefix + "copy <player>`\n\n"
                msg += "**Example:** `" + prefix + "copy @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by Look-Alike's."
                return [Mailbox().respond(msg,True)]
            if user_role == "Look-Alike":
                help_msg += "`" + prefix + "copy` - Imitate another player. (Look-Alike only)\n"

            '''holify'''
            # The Priest's command
            if is_command(message, ['holify', 'sacrify', 'water']) and user_role == "Priest":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.nightly_kill(user_id,target[0])]
            if is_command(message, ['holify', 'sacrify', 'water'], True) and user_role == "Priest":
                msg = "**Usage:** Throw Holy water on a player.\n\n`" + prefix + "holify <player>`\n\n"
                msg += "**Example:** `" + prefix + "holify @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by the Priest."
                return [Mailbox().respond(msg,True)]
            if user_role == "Priest" and user_undead == 0:
                help_msg += "`" + prefix + "holify` - Holify a player. (Priest only)\n"

            '''purify'''
            # The Priestess' command
            if is_command(message, ['heal', 'light', 'purify', 'sacrify']) and user_role == "Priestess":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.purify(user_id,target[0])]
            if is_command(message, ['heal', 'light', 'purify', 'sacrify'], True) and user_role == "Priestess":
                msg = "**Usage:** Purify a player.\n\n`" + prefix + "purify <player>`\n\n"
                msg += "**Example:** `" + prefix + "purify @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by the Priestess."
                return [Mailbox().respond(msg,True)]
            if user_role == "Priestess" and user_undead == 0:
                help_msg += "`" + prefix + "purify` - Purify a player. (Priestess only)\n"

            '''threaten'''
            # The Raven's command
            if is_command(message, ['threaten', 'raven']) and user_role == "Raven":
                # TODO
                return todo()
            if is_command(message, ['threaten', 'raven'], True) and user_role == "Raven":
                msg = "**Usage:** Threaten a player.\n\n`" + prefix + "threaten <player>`\n\n"
                msg += "**Example:** `" + prefix + "threaten @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by the Raven."
                return [Mailbox().respond(msg,True)]
            if user_role == "Raven" and user_undead == 0:
                help_msg += "`" + prefix + "threaten` - Threaten a player. (Raven only)\n"

            '''reveal'''
            # The Royal Knight's command
            if is_command(message, ['end', 'prevent', 'reveal', 'stop']) and user_role == "Royal Knight":
                # TODO
                return todo()
            if is_command(message, ['end', 'prevent', 'reveal', 'stop'], True) and user_role == "Royal Knight":
                msg = "**Usage:** Prevent a lynch.\n\n`" + prefix + "prevent`\n\n"
                msg += "**Example:** `" + prefix + "prevent`. "
                msg += "This command can only be used by the Royal Knight."
                return [Mailbox().respond(msg,True)]
            if user_role == "Royal Knight":
                help_msg += "`" + prefix + "prevent` - Prevent the public lynch from happening. (Royal Knight only)\n"

            '''life'''
            # The witch' command to use her life potion
            if is_command(message, ['heal', 'life', 'save']) and user_role == "Witch":
                # TODO
                return todo()
            if is_command(message, ['heal', 'life', 'save'], True) and user_role == "Witch":
                msg = "**Usage:** Use potion of life.\n\n`" + prefix + "save`\n\n"
                msg += "**Example:** `" + prefix + "save`. "
                msg += "This command can only be used by the Witch."
                return [Mailbox().respond(msg,True)]
            if user_role == "Witch" and user_undead == 0:
                help_msg += "`" + prefix + "life` - Brew life potion. (Witch only)\n"

            '''death'''
            # The witch' command to use her death potion
            if is_command(message, ['death', 'kill', 'murder', 'poison']) and user_role == "Witch":
                # TODO
                return todo()
            if is_command(message, ['death', 'kill', 'murder', 'poison'], True) and user_role == "Witch":
                msg = "**Usage:** Use potion of death.\n\n`" + prefix + "kill <player>`\n\n"
                msg += "**Example:** `" + prefix + "kill @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by the Witch."
                return [Mailbox().respond(msg,True)]
            if user_role == "Witch" and user_undead == 0:
                help_msg += "`" + prefix + "death` - Brew death potion. (Witch only)\n"

            '''çurse'''
            # The curse caster's command
            if is_command(message, ['cast', 'corrupt', 'curse']) and user_role == "Curse Caster":
                # TODO
                return todo()
            if is_command(message, ['cast', 'corrupt', 'curse'], True) and user_role == "Curse Caster":
                msg = "**Usage:** Cast a curse on a player.\n\n`" + prefix + "curse <player>`\n\n"
                msg += "**Example:** `" + prefix + "curse @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by the Curse Caster."
                return [Mailbox().respond(msg,True)]
            if user_role == "Curse Caster" and user_undead == 0:
                help_msg += "`" + prefix + "curse` - Curse a player. (Curse Caster only)\n"

            '''infect'''
            # The infected wolf's command
            if is_command(message, ['cough', 'infect', 'sneeze', 'turn']) and user_role == "Infected Wolf":
                # TODO
                return todo()
            if is_command(message, ['cough', 'infect', 'sneeze', 'turn'], True) and user_role == "Infected Wolf":
                msg = "**Usage:** Turn a player into a Wolf.\n\n`" + prefix + "infect <player>`\n\n"
                msg += "**Example:** `" + prefix + "infect @Randium#6521`\nThe command is compatible with emojis as a replacement for user mentions. "
                msg += "This command can only be used by the Infected Wolf."
                return [Mailbox().respond(msg,True)]
            if user_role == "Infected Wolf" and user_undead == 0:
                help_msg += "`" + prefix + "infect` - Infect a player. (Imfected Wolf only)\n"

            '''devour'''
            # The Lone wolf's command
            if is_command(message, ['chew', 'devour', 'eat', 'kill', 'munch']) and user_role == "Lone Wolf":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.nightly_kill(user_id,target[0])]
            if is_command(message, ['chew', 'devour', 'eat', 'kill', 'munch'], True) and user_role == "Lone Wolf":
                # TODO
                return todo()
            if user_role == "Lone Wolf" and user_undead == 0:
                help_msg += "`" + prefix + "devour` - Kill a player. (Lone Wolf only)\n"

            '''disguise'''
            # The tanner's command
            if is_command(message, ['change', 'cloth', 'disguise', 'hide']) and user_role == "Tanner":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                disguise = check.roles(message,1)
                if not disguise:
                    return [Mailbox().respond("**INVALID SYNTAX:** \nPlease make sure to provide a role.")]
                return [func.disguise(user_id,target[0],disguise[0])]
            if is_command(message, ['change', 'cloth', 'disguise', 'hide'], True) and user_role == "Tanner":
                # TODO
                return todo()
            if user_role == "Tanner" and user_undead == 0:
                help_msg += "`" + prefix + "disguise` - Disguise a player. (Tanner only)\n"

            '''inspect'''
            # The Warlock's command
            if is_command(message, ['forsee', 'inspect', 'see', 'tell']) and user_role == "Warlock":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.see(user_id,target[0])]
            if is_command(message, ['forsee', 'inspect', 'see', 'tell'], True) and user_role == "Warlock":
                # TODO
                return todo()
            if user_role == "Warlock" and user_undead == 0:
                help_msg += "`" + prefix + "see` - Inspect a player's role. (Warlock only)\n"

            '''devour'''
            # The white werewolf's command
            if is_command(message, ['chew', 'devour', 'eat', 'kill', 'munch']) and user_role == "White Werewolf":
                # TODO
                return todo()
            if is_command(message, ['chew', 'devour', 'eat', 'kill', 'munch'], True) and user_role == "White Werewolf":
                # TODO
                return todo()
            if user_role == "White Werewolf" and user_undead == 0:
                help_msg += "`" + prefix + "devour` - Kill a fellow wolf. (White Werewolf Only)\n"

            '''wager'''
            # The devil's command
            if is_command(message, ['choose', 'wager']) and user_role == "Devil":
                # TODO
                return todo()
            if is_command(message, ['choose', 'wager'], True) and user_role == "Devil":
                # TODO
                return todo()
            if user_role == "Devil":
                help_msg += "`" + prefix + "wager` - Send the Devil's Wager to a player. (Devil only)\n"

            '''enchant'''
            # The flute player's command
            if is_command(message, ['enchant', 'flute']) and user_role == "Flute Player":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.enchant(user_id,target[0])]
            if is_command(message, ['enchant', 'flute'], True) and user_role == "Flute Player":
                # TODO
                return todo()
            if user_role == "Flute Player":
                help_msg += "`" + prefix + "enchant` - Enchant a player.\n"

            '''unite'''
            # The horseman's command
            if is_command(message, ['apocalypse', 'clean', 'unite']) and user_role == "Horseman":
                target = check.users(message,1,True,True)
                if not target:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.nightly_kill(user_id,target[0])]
            if is_command(message, ['apocalypse', 'clean', 'unite'], True) and user_role == "Horseman":
                # TODO
                return todo()
            if user_role == "Horseman" and user_undead == 0:
                help_msg += "`" + prefix + "unite` - Apocalypse a player. (Horsemen only)\n"

            '''guess'''
            # The ice king's command to add a guess about a user to their list.
            # Note that this command could/should be usable at any time, as long as the submit command isn't
            if is_command(message, ['add', 'guess', 'freeze']) and user_role == "Ice King":
                target = check.users(message,1,True,True)
                if not target:
                    return [func.freeze(user_id)]
                guessed_role = check.roles(message,1,True)
                if not guessed_role:
                    return [func.freeze(user_id,target[0])]
                return [func.freeze(user_id,target[0],guessed_role[0])]
            if is_command(message, ['add', 'guess', 'freeze'], True) and user_role == "Ice King":
                # TODO
                return todo()
            if user_role == "Ice King":
                help_msg += "`" + prefix + "guess` - Guess a player's role. (Ice King only)\n"

            '''submit'''
            # The ice king's command to submit the list of people of whom they have guessed their roles.
            if is_command(message, ['guess_that', 'freeze_all', 'submit']) and user_role == "Ice King":
                return [func.freeze_all(user_id)]
            if is_command(message, ['guess_that', 'freeze_all', 'submit'], True) and user_role == "Ice King":
                # TODO
                return todo()
            if user_role == "Ice King":
                help_msg += "`" + prefix + "submit` - Submit list of guessed players. (Ice King only)\n"

            '''powder'''
            # Powder a player
            if is_command(message, ['creeper', 'powder']) and user_role == "Pyromancer":
                # TODO
                return todo()
            if is_command(message, ['creeper', 'powder'], True) and user_role == "Pyromancer":
                # TODO
                target = check.users(message, amount=1, must_be_participant=True)
                if not target:
                    return [Mailbox().embed(destination=message.channel, embed=Embed(
                    title="Invalid user", description="Please mention a user (either by mention, or by emoji)"
                        .format(user=message.author.id, target=target[0].id)), temporary=True)]

                func.powder(message.author.id, target[0].id)
                return [Mailbox().embed(destination=message.channel, embed=Embed(
                    title="Powdered a participant", description="<@{user}> powdered <@{target}>"
                        .format(user=message.author.id, target=target[0].id)))]
            if user_role == "Pyromancer":
                help_msg += "`" + prefix + "powder` - Powder a player. (Pyromancer only)\n"

            '''abduct'''
            # To kidnap players
            if is_command(message, ['abduct', 'add', 'kidnap', 'swamp']) and user_role == "The Thing":
                # TODO
                return todo()
            if is_command(message, ['abduct', 'add', 'kidnap', 'swamp'], True) and user_role == "The Thing":
                # TODO
                return todo()
            if user_role == "The Thing" and user_undead == 0:
                help_msg += "`" + prefix + "abduct` - Choose a player to abduct. (The Thing only)\n"

            '''create_swamp'''
            # To create a new swamp with all victims
            if is_command(message,
                          ['abduct_all', 'create_swamp', 'start_cliche_horror_movie']) and user_role == "The Thing":
                # TODO
                return todo()
            if is_command(message, ['abduct_all', 'create_swamp', 'start_cliche_horror_movie'],
                          True) and user_role == "The Thing":
                # TODO
                return todo()
            if user_role == "The Thing" and user_undead == 0:
        	    help_msg += "`" + prefix + "create_swamp` - Create swamp with chosen players. (The Thing only)\n"
    elif is_command(message, [
        'abduct', 'abduct_all', 'add', 'apocalypse', 'assassinate', 'aura',
        'barber_kill', 'bark', 'become', 'cast', 'cc', 'change', 'chew', 'choose',
        'clean', 'cloth', 'copy', 'corrupt', 'cough', 'create_swamp', 'creeper',
        'crowd', 'curse', 'cut', 'death', 'devour', 'disguise', 'donate', 'eat',
        'enchant', 'end', 'execute', 'exercise', 'exorcise', 'flute', 'follow',
        'forsee', 'freeze', 'freeze_all', 'fuck', 'give_amulet', 'give_cc', 'guess',
        'guess_that', 'heal', 'hide', 'holify', 'hook', 'hunt', 'imitate', 'infect',
        'info', 'inspect', 'kidnap', 'kill', 'kiss', 'knit', 'knot', 'life', 'light',
        'love', 'melt', 'mirror', 'more_cc', 'munch', 'murder', 'myrole', 'poison',
        'powder', 'prevent', 'purify', 'raven', 'remove', 'resemble', 'reveal',
        'sacrify', 'save', 'see', 'seek', 'shoot', 'silence', 'sleep', 'sneeze',
        'start_cliche_horror_movie', 'stop', 'submit', 'swamp', 'tell', 'threaten',
        'turn', 'undoom', 'unfreeze', 'unite', 'vision', 'wager', 'water',]):
        return [Mailbox().respond(PERMISSION_MSG.format("Participant"), True)]


    # =============================================================
    #
    #                         EVERYONE
    #
    # =============================================================

    help_msg += '\n\n'

    '''age'''
    # Allows users to set their age.
    if is_command(message, ['age']):
        # TODO
        return todo()
    if is_command(message, ['age'], True):
        msg = "**USAGE:** This command is used to set your age. \n\n`" + prefix + "age<number>\n\n**Example:** `!age 19`"
        return [Mailbox().respond(msg,True)]
    help_msg += "`" + prefix + "age` - Set your age.\n"

    '''profile'''
    # This command allows one to view their own profile
    # When giving another player's name, view that player's profile
    if is_command(message, ['profile']):
        # TODO
        return todo()
    if is_command(message, ['profile'], True):
        msg = "**USAGE:** The use of this command is to check your own profile, you can check other peoples profiles by adding their name. \n\n`" + prefix + "profile <user>`\n\n**Example:** `!profile @Randium#6521`"
        return [Mailbox().respond(msg,True)]
    help_msg += "`" + prefix + "profile` - See a player's profile.\n"

    '''shop'''
    # This command creates a new shop instance in the channel it was sent in
    # This function returns a mailbox
    if is_command(message, ['shop']):
        return [Mailbox().shop(message.channel)]

    '''signup'''
    # This command signs up the player with their given emoji, assuming there is no game going on.
    if is_command(message, ['signup']):
        if dy.get_signup() == 0:
            return [Mailbox().respond("I am sorry, but you currently cannot sign up yet! Ask Game Masters to open the signups.", True)]

        if dy.get_signup() == 1 and len(db.player_list()) >= max_participants:
            return [Mailbox().respond("I am terribly sorry! We have closed the signups because the game's full!\nPlease try again later or contact the Game Masters.")]

        emojis = check.emojis(message)
        choice_emoji = ""

        if emojis == False:
            msg = "**Incorrect syntax:** `" + prefix + "signup <emoji>`\n\nExample: `" + prefix + "signup :smirk:`"
            return [Mailbox().respond(msg, True)]

        for emoji in emojis:
            if emoji_to_player(emoji) == None:
                choice_emoji = emoji
                break

        if isParticipant(user_id, True, True):
            if choice_emoji == "":
                return [Mailbox().respond(
                    "You are already signed up with the {} emoji! Also, your emoji was occupied.".format(
                        db_get(user_id, 'emoji')), True)]
            db_set(user_id, 'emoji', choice_emoji)
            reaction = Mailbox().respond(
                "You have successfully changed your emoji to the {} emoji!".format(choice_emoji))
            return [reaction.spam("<@{}> has changed their emoji to the {} emoji.".format(user_id, choice_emoji))]

        if choice_emoji == "":
            if len(emojis) == 1:
                return [Mailbox().respond("I am sorry! Your chosen emoji was already occupied.", True)]
            return [Mailbox().respond("I am sorry, but all of your given emojis were already occupied! Such bad luck.",
                                      True)]
        signup(user_id, message.author.name, choice_emoji)
        reaction = Mailbox().respond("You have successfully signed up with the {} emoji!".format(choice_emoji))

        if dy.get_signup() == 1:
            reaction.spam("<@{}> has signed up with the {} emoji.".format(user_id, choice_emoji))
        else:
            reaction.spam("<@{}> has started to spectate.".format(user_id))
        return [reaction]
    if is_command(message, ['signup'], True):
        msg = "**Usage:** `" + prefix + "signup <emoji>`\n\nExample: `" + prefix + "signup :smirk:`"
        return [Mailbox().respond(msg, True)]
    help_msg += "`" + prefix + "signup` - Signup for a game.\n"

    # -----------------------
    # Easter eggs
    if is_command(message,['randiumlooks','whatdoesrandiumlooklike']):
        answer = Mailbox()
        for phrase in eggs.randiumlooks():
            answer.respond(phrase)
        return [answer]

    # --------------------------------------------------------------
    #                          HELP
    # --------------------------------------------------------------
    help_msg += "\n\n*If you have any more questions, feel free to ask any of the Game Masters!*"

    '''help'''
    if is_command(message,['help']) and is_command(message,['help'],True) == False:
        return [Mailbox().respond(help_msg,True)]
    if is_command(message,['help'],True):
        answer = Mailbox().respond("Hey there! `" + prefix + "help` will give you a list of commands that you can use.")
        answer.respond_add("\nIf you have any questions, feel free to ask any of the Game Masters!")
        return [answer]

    if message.content.startswith(prefix):
        return [Mailbox().respond("Sorry bud, couldn't find what you were looking for.", True)]

    return []

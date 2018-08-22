# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from discord import Embed

import interpretation.check as check
import roles_n_rules.functions as func
from config import max_cc_per_user, season, universal_prefix as unip
from config import ww_prefix as prefix
from interpretation.check import is_command
from main_classes import Mailbox
from management.position import valid_distribution
from management.db import isParticipant, personal_channel, db_get, db_set, signup, emoji_to_player, channel_get, \
    is_owner, get_channel_members
from story_time.commands import cc_goodbye, cc_welcome
import story_time.eastereggs as eggs

PERMISSION_MSG = "Sorry, but you can't run that command! You need to have **{}** permissions to do that."

def todo():
    return [Mailbox().respond("I am terribly sorry! This command doesn't exist yet!", True)]


def process(message, isGameMaster=False, isAdmin=False, isPeasant=False):
    user_id = message.author.id
    message_channel = message.channel.id
    user_role = db_get(user_id, 'role')

    help_msg = "**List of commands:**\n"

    '''testpoll'''
    if is_command(message,['poll','testpoll']):
        return [Mailbox().new_poll(message.channel.id,'lynch',message.author.id,message.content.split(' ',1)[1])]

    '''dist'''
    if is_command(message,['dist','checkdist','check_dist']):
        roles = check.roles(message)
        if not roles:
            return [Mailbox().respond("You gotta provide some roles, bud!",True)]
        judgment = valid_distribution(roles)
        if not judgment:
            return [Mailbox().respond("Sorry, that's an invalid role distribution!",True)]
        return [Mailbox().respond(judgment,True)]

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
    elif is_command(message, ['delete_category']):
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
            # TODO
            return todo()
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
            db_set(user[0], 'fakerole', role[0])
            return [Mailbox().spam("You have successfully given <@{}> the role of the `{}`!".format(user[0], role[0]))]

        if is_command(message, ['assign'], True):
            msg = "**Usage:** Give a player a specific role\n\n`" + prefix + "assign <user> <role>`\n\nExample: `" + prefix
            msg += "assign @Randium#6521 Innocent`\nThis command can only be used by Game Masters."
            return [Mailbox().spam(msg)]
        help_msg += "`" + prefix + "assign` - Give player a given role.\n"

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
            db_set(target[0],'ccs',ccs_owned-number)
            return [Mailbox().spam("<@{}> has received {} extra conspiracy channel slots.")]
        if is_command(message,['donate','give_cc','more_cc'],True):
            return [Mailbox().respond("**Usage:** Give a player more cc's.\n\n`" + prefix + "donate <user> <number>`\n\n**Example:** `" + prefix + "donate @Randium#6521 3`",True)]
        help_msg += "`" + prefix + "donate` - Give a player more cc's.\n"

        '''signup'''
        # This command signs up the player with their given emoji, assuming there is no game going on.
        if is_command(message, ['signup']):
            target = check.users(message)
            emojis = check.emojis(message)
            choice_emoji = ""

            if not target:
                return [Mailbox("Target not found! Please provide us with a user!",True)]

            user_id = target[0]

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
                        "They are already signed up with the {} emoji! Also, the emoji was occupied.".format(
                            db_get(user_id, 'emoji')), True)]
                db_set(user_id, 'emoji', choice_emoji)
                reaction = Mailbox().respond(
                    "You have successfully changed their emoji to the {} emoji!".format(choice_emoji))
                return [reaction.spam("<@{}> has changed their emoji to the {} emoji.".format(user_id, choice_emoji))]

            if choice_emoji == "":
                if len(choice_emoji) == 1:
                    return [Mailbox().respond("I am sorry! Your chosen emoji was already occupied.", True)]
                return [Mailbox().respond("I am sorry, but all of your given emojis were already occupied! Such bad luck.",
                                        True)]
            signup(user_id, message.author.name, choice_emoji)
            reaction = Mailbox().respond("You have successfully signed them up with the {} emoji!".format(choice_emoji))
            return [reaction.spam("<@{}> was signed up with the {} emoji.".format(user_id, choice_emoji))]
        if is_command(message, ['signup'], True):
            msg = "**Usage:** `" + prefix + "signup <emoji>`\n\nExample: `" + prefix + "signup :smirk:`"
            return [Mailbox().respond(msg, True)]
        help_msg += "`" + prefix + "signup` - Sign a player up for a game.\n"



    elif is_command(message, ['addrole','assign','day','donate','night','open_signup','signup','whois']):
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
                answer.spam("**Warning:** <@{}> has reached the maximum amount of conspiracy channels!\n")
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
            embed.set_footer(text='Conspiracy Channel Information requested by ' + message.author.nick)
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


    # =============================================================
    #
    #                         EVERYONE
    #
    # =============================================================

    help_msg += '\n\n'

    # -----------------------
    # Easter eggs
    if is_command(message,['randiumlooks','whatdoesrandiumlooklike']):
        answer = Mailbox()
        for phrase in eggs.randiumlooks():
            answer.respond(phrase,True)
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

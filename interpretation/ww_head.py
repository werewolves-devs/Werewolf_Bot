# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from management.db import isParticipant, personal_channel, db_get, db_set, signup, emoji_to_player, channel_get, is_owner, get_channel_members
from roles_n_rules.commands import cc_goodbye
from interpretation.check import is_command
from config import max_cc_per_user
from config import ww_prefix as prefix
from main_classes import Mailbox, Message
from discord import Embed
import roles_n_rules.functions as func
import interpretation.check as check
import discord

def todo():
    return [Mailbox().spam("I am terribly sorry! This command doesn't exist yet!",True)]

def process(message, isGameMaster = False, isAdmin = False):

    user_id = message.author.id
    message_channel = message.channel.id
    user_role = db_get(user_id,'role')


    '''evaluate'''
    if is_command(message,['eval']):
        return [Mailbox(True)]

    '''testpoll'''
    if is_command(message,['poll','testpoll']):
        return [Mailbox().new_poll(message.channel.id,'lynch',message.author.id,message.content.split(' ',1)[1])]

    # =============================================================
    #
    #                         ADMINISTRATOR
    #
    # =============================================================
    if isAdmin == True:

        '''delete_category'''
        # This command is used to entirely delete a category and all channels in it
        # (Note that this will A: take a while due to ratelimits and B: Spam the audit log)
        # Moderation should be used to ensure this command is not used outside of where it's allowed
        if is_command(message,['delete_category']):
            int_table = check.numbers(message)
            if int_table == False:
                return [Mailbox().respond("**Invalid syntax:** Missing category id.\n\n`" + prefix + "delete_category <category id>`")]
            answer = Mailbox()
            for id in int_table:
                answer.delete_category(id)
            return [answer]
        if is_command(message,['delete_category'],True):
            msg = "**Usage:** Deletes an entire category and all channels in it.\n\n`" + prefix + "delete_category <id>`\n\n**Example:** `" + prefix + "delete_category 457264810363584513`"
            msg += "\nThe command does not accept multiple categories. This command can only be used by Game Masters."
            return [Mailbox().respond(msg,True)]

    # =============================================================
    #
    #                         GAME MASTERS
    #
    # =============================================================
    if isGameMaster == True:

        '''addrole'''
        # Before the game starts, a list of roles is kept track of.
        # That list is the list of roles that will be dealt among the participants.
        # If the list is greater than the amount of participants, some random roles will be left out.
        # The game cannot start as long as this list is incomplete.
        if is_command(message,['addrole']):
            # TODO
            return todo()
        if is_command(message,['addrole'],True):
            msg = "**Usage:** Add a role to the game pool\n\n`" + prefix + "addrole <role>`\n\n**Example:** `" + prefix + "addrole Innocent`"
            msg += "\nThe command accepts multiple roles. This command can only be used by Game Masters."
            return [Mailbox().respond(msg,True)]

        '''assign'''
        # This command is used at the start of the game to assign all roles.
        # This will actually set their "fakerole" value, which will be transferred to their actual role once the game starts.
        if is_command(message,['assign']):
            role = check.roles(message,1)
            user = check.users(message,1)

            if role == False:
                return [Mailbox().respond("No role provided! Please provide us with a role!")]
            if user == False:
                return [Mailbox().respond("No user found! Please provide us with a user!")]
            if isParticipant(user[0],True,True) == False:
                return [Mailbox().respond("I am terribly sorry. You cannot assign a role to a user that hasn\'t signed up!")]

            db_set(user[0],'role',role[0])
            return [Mailbox().spam("You have successfully given <@{}> the role of the `{}`!".format(user[0],role[0]))]

        if is_command(message,['assign'],True):
            msg = "**Usage:** Give a player a specific role\n\n`" + prefix + "assign <user> <role>`\n\nExample: `" + prefix
            msg += "assign @Randium#6521 Innocent`\nThis command can only be used by Game Masters."
            return [Mailbox().spam(msg)]

        '''day'''
        # This command is used to initialize the day.
        if is_command(message,['day']):
            # TODO
            return todo()
        if is_command(message,['day'],True):
            msg = "**Usage:** Initiate the day if this does not happen automatically.\n\n"
            msg += "`" + prefix + "day`\n\nThis command can only be used by Game Masters."
            return [Mailbox().respond(msg,True)]

        '''night'''
        # This command is used to initialize the day.
        if is_command(message,['night']):
            # TODO
            return todo()
        if is_command(message,['night'],True):
            msg = "**Usage:** Initiate the night if this does not happen automatically.\n\n"
            msg += "`" + prefix + "night`\n\nThis command can only be used by Game Masters."
            return [Mailbox().respond(msg,True)]

        '''open_signup'''
        # This command is started when a new game can be started.
        # Make sure the bot has reset itself beforehand.
        if is_command(message,['open_signup']):
            # TODO
            return todo()
        if is_command(message,['open_signup'],True):
            msg = "**Usage:** Allow users to sign up for a new game.\n\n`" + prefix + "open_signup`\n\n"
            msg += "This command can only be used by Game Masters."
            return [Mailbox().respond(msg,True)]

        '''whois'''
        # This command reveals the role of a player.
        # To prevent spoilers, the response isn't made in the message's channel, but rather in the bot spam channel.
        if is_command(message,['whois']):
            user_table = check.users(message)
            identities = Mailbox()

            if user_table == False:
                return [Mailbox().respond("**ERROR:** No user provided!",True)]

            for user in user_table:
                emoji = db_get(user,'emoji')
                role = db_get(user,'role')
                member = message.channel.guild.get_member(int(user))
                if emoji == None or role == None:
                    identities.spam("**ERROR:** Could not find user <@{}> in database.".format(user))
                elif member == None:
                    identities.spam("I am sorry, but I couldn\'t find <@{}> on this server! Try again, please!".format(user))
                else:
                    special_tags = ""
                    if int(db_get(user,'abducted')) == 1:
                        special_tags += '[Abducted] '
                    if int(db_get(user,'bites')) > 0:
                        special_tags += '[Bitten] '
                    if int(db_get(user,'demonized')) == 1:
                        special_tags += '[Demonized] '
                    if db_get(user,'fakerole') != role:
                        special_tags += "[Disguised as {}] ".format(db_get(user,'fakerole'))
                    if int(db_get(user,'enchanted')) == 1:
                        special_tags += "[Enchanted] "
                    if int(db_get(user,'frozen')) == 1:
                        special_tags += '[Frozen] '
                    if int(db_get(user,'powdered')) == 1:
                        special_tags += '[Powdered] '
                    if int(db_get(user,'souls')) > -1:
                        special_tags += '[Soulless One] '
                    if int(db_get(user,'threatened')) > 0:
                        special_tags += "[Threatened] "
                    if int(db_get(user,'undead')) == 1:
                        special_tags += '[Undead] '
                    if special_tags == "":
                        special_tags += "None"
                    embed = Embed(color=0xcd9e00, title='User Info')
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.add_field(name = "Name", value = "<@{}>".format(user))
                    embed.add_field(name = "Emoji", value = emoji)
                    embed.add_field(name = "Role", value = role)
                    embed.add_field(name = "Attributes", value = special_tags)
                    embed.set_footer(text='Participant Information requested by ' + message.author.name)
                    identities.embed(embed,'spam')

            return [identities]

        if is_command(message,['whois'],True):
            msg = "**Usage:** Gain all the wanted info about a player.\n\n`" + prefix + "whois <user1> <user2> ...`\n\n"
            msg += "**Example:** `" + prefix + "whois @Randium#6521`\nThe command will only answer in the botspam-channel, "
            msg += "to prevent any accidental spoilers from occurring. This command can only be used by Game Masters."
            return [Mailbox().respond(msg,True)]

    # =============================================================
    #
    #                         PARTICIPANTS
    #
    # =============================================================

    if isParticipant(user_id):

        '''add'''
        # This command allows users to add users to a conspiracy.
        # This command will not trigger if the user doesn't own the conspiracy channel.
        if is_command(message,['add']):
            members_to_add = check.users(message)
            if members_to_add == False:
                return [Mailbox().respond("I am sorry! I couldn't find the user you were looking for!",True)]
            if is_owner(user_id,message_channel) == False:
                return [Mailbox().respond("I\'m sorry, you can only use this in conspiracy channels where you are the owner!")]

            command = Mailbox()
            for member in members_to_add:
                if isParticipant(member) == False:
                    command.edit_cc(message_channel,member,4)
                elif int(db_get(member,'abducted')) == 1:
                    command.edit_cc(message_channel,member,3)
                elif int(db_get(member,'frozen')) == 1:
                    command.edit_cc(message_channel,member,2)
                else:
                    command.edit_cc(message_channel,member,1)
            return [command.respond("Please wait whilst I save your changes...")]

        if is_command(message,['add'],True):
            msg = "**Usage:** Add a user to the existing conspiracy channel.\n\n`" + prefix + "add <user>`\n\n"
            msg += "**Example:** `" + prefix + "add @Randium#6521`\nThis command can only be used by the owner of "
            msg += "the conspiracy channel. To see who owns a given conspiracy channel, type `" + prefix + "info`."
            return [Mailbox().respond(msg,True)]

        '''cc'''
        # This command allows users to create a conspiracy channel.
        if is_command(message, ['cc']):
            if len(message.content.split(' ')) < 2:
                    return [Mailbox().respond("**Invalid syntax:**\n\n`" + prefix + "cc <name> <user1> <user2> <user3> ...`\n\n**Example:** `" + prefix + "cc the_cool_guys @Randium#6521`")]

            channel_members = check.users(message)
            if channel_members == False:
                channel_members = []
            if user_id not in channel_members:
                channel_members.append(user_id)

            num_cc_owned = int(db_get(user_id,'ccs'))

            if num_cc_owned >= max_cc_per_user:
                answer = Mailbox().dm("You have reached the amount of conspiracy channels one may own!", user_id)
                return [answer.dm("If you want more conspiracy channels, please request permission from one of the Game Masters.", user_id)]

            db_set(user_id,'ccs',num_cc_owned + 1)
            return [Mailbox().create_cc(message.content.split(' ')[1], user_id, channel_members).spam("<@{}> has created a *conspiracy channel* called {}!".format(user_id,message.content.split(' ')[1]))]

        if is_command(message,['cc'],True):
            msg = "**Usage:** create a *conspiracy channel*, a private channel where one can talk with a selected group of players.\n\n"
            msg += "`" + prefix + "cc <name> <user1> <user2> <user3> ...`\n\n**Example:** `" + prefix + "cc the_cool_guys @Randium#6521`\n"
            msg += "Please do not abuse this command to create empty channels without a purpose. Abuse will be noticed and dealt with accordingly."
            return [Mailbox().respond(msg,True)]

        '''info'''
        # This command allows users to view information about a conspiracy channel.
        # Says the user must be in a cc if they're not.
        if is_command(message,['info']):
            guild = message.channel.guild
            try:
                owner_id = channel_get(message.channel.id,'owner')
            except:
                return[Mailbox().respond('Sorry, but it doesn\'t look like you\'re in a CC! If you are, please alert a Game Master as soon as possible.')]
            if owner_id != None:
                owner_object = guild.get_member(int(owner_id))
            else:
                owner_object = None
            embed = Embed(color=0x00cdcd, title='Conspiracy Channel Info')
            if owner_object != None and owner_id != None:
                embed.add_field(name='Channel Owner', value='<@' + owner_id + '>')
                embed.set_thumbnail(url=owner_object.avatar_url)
            elif owner_id == None:
                return [Mailbox().respond('Sorry, but it doesn\'t look like you\'re in a CC! If you are, please alert a Game Master as soon as possible.')]
            else:
                try:
                    owner_name = db_get(owner_id,'name')
                    if str(owner_name) == 'None':
                        owner_name = 'Sorry, an error was encountered. Please alert a Game Master.'
                except:
                    owner_name == 'Sorry, an error was encountered. Please alert a Game Master.'

                embed.add_field(name='Channel Owner', value=owner_name)
            member_text = ""
            for member in get_channel_members(message.channel.id):
                member_text += "<@" + str(member) + "> "
            embed.add_field(name='Channel Name', value=message.channel.name)
            embed.add_field(name='Participants', value=member_text)
            embed.set_footer(text='Conspiracy Channel Information requested by ' + message.author.nick)
            return [Mailbox().embed(embed, message.channel.id)]
        if is_command(message,['info'],True):
            msg = "**Usage:** Gain information about a conspiracy channel.\n\n`" + prefix + "info`\n\n"
            msg += "Try it! You\'ll see what it does."
            return [Mailbox().respond(msg,True)]

        '''myrole'''
        # This command sends the user's role back to them in a DM.
        if is_command(message,['myrole']):
            if int(db_get(message.author.id,'undead')) == 0:
                return [Mailbox().dm("Your role is **{}**.".format(db_get(message.author.id,'role')), message.author.id,False,[db_get(message.author.id,'emoji')])]
            return [Mailbox().dm("You pretend to be a **{}**, while you are secretly an **Undead**!".format(db_get(message.author.id,'role')),message.author.id)]
        if is_command(message,['myrole'],True):
            msg = "**Usage:** Get a DM of what your role is.\n\n`" + prefix + "myrole`\n\n"
            msg += "This command may sound silly, but it could be useful if the player is confused about whether certain "
            msg += "scenarios have changed their role or not."
            return [Mailbox().respond(msg,True)]

        '''remove'''
        # This command removes a given user from a conspiracy channel.
        # A user should not get removed if they're the channel owner.
        if is_command(message,['remove']):
            members_to_remove = check.users(message)
            if is_owner(user_id,message_channel) == False:
                return [Mailbox().respond("I\'m sorry, but you cannot use this command over here!")]
            command = Mailbox().respond("Looks like we\'ll have to say goodbye!")
            for member in members_to_remove:
                if is_owner(member,message_channel) == True:
                    command.respond("Sorry bud, ya can\'t remove the cc's owner! Blame the people who used to do this on purpose.")
                else:
                    command.edit_cc(member,message_channel,0)
                    command.respond(cc_goodbye(member))
            return [command]

        if is_command(message,['remove'],True):
            msg = "**Usage:** Remove a user from a conspiracy channel.\n\n`" + prefix + "remove <user>`\n\n"
            msg += "**Example:** `" + prefix + "remove @Randium#6521`\nThis command can only be used by the conspiracy channel owner."
            return [Mailbox().respond(msg,True)]

        # =======================================================
        #                ROLE SPECIFIC COMMANDS
        # =======================================================
        if personal_channel(user_id,message_channel) == True:

            '''give_amulet'''
            # This command can be executed by everyone, but only in one channel.
            # That's the amulet channel.
            # To be worked out how exactly.
            if is_command(message,['give_amulet']):
                # TODO
                return todo()
            if is_command(message,['give_amulet'],True):
                # TODO
                return todo()

            '''assassinate'''
            # Assassin's command; kill a victim
            if is_command(message,['assassinate','kill']) and user_role == "Assassin":
                target = check.users(message,1,True,True)
                if target == False:
                    return [Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)]
                return [func.nightly_kill(user_id,target[0])]

            if is_command(message,['assassinate','kill'],True) and user_role == "Assassin":
                msg = "**Usage:** Kill another player.\n\n`" + prefix + "kill <player>`\n\n"
                msg += "**Example:** `" + prefix + "kill @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by Assassins during the night."
                return [Mailbox().respond(msg,True)]

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

            '''barber_kill'''
            # Barber kill - to assassinate a victim during the day
            if is_command(message,['assassinate','barber_kill','cut']) and user_role == "Barber":
                # TODO
                return todo()
            if is_command(message,['assassinate','barber_kill','cut'],True) and user_role == "Barber":
                msg = "**Usage:** Kill a player during the day.\n\n`" + prefix + "cut <player>`\n\n"
                msg += "**Example:** `" + prefix + "cut @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by barbers during the day. This command only works once, so choose wisely."

            '''seek'''
            # Crowd seeker's power
            if is_command(message,['crowd','seek']) and user_role == "Crowd Seeker":
                # TODO
                return todo()
            if is_command(message,['crowd','seek'],True) and user_role == "Crowd Seeker":
                msg = "**Usage:** Inspect a player's role.\n\n`" + prefix + "seek <player> <role>`\n\n"
                msg += "**Example:** `" + prefix + "seek @Randium#621 Innocent`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by crowd seekers during the first night."

            '''kiss'''
            # Cupid's power to fall in love with someone.
            if is_command(message,['kiss','love','shoot']) and user_role == "Cupid":
                # TODO
                return todo()
            if is_command(message,['kiss','love','shoot'],True) and user_role == "Cupid":
                msg = "**Usage:** Fall in love with another player.\n\n`" + prefix + "love <player>`\n\n"
                msg += "**Example:** `" + prefix + "love @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by the Cupid during the night."

            '''follow'''
            # The command that allows the dog to choose a side.
            if is_command(message,['bark','become','choose','follow']) and user_role == "Dog":
                # TODO
                return todo()
            if is_command(message,['bark','become','choose','follow'],True) and user_role == "Dog":
                msg = "**Usage:** Choose a role to play as.\n\n`" + prefix + "choose <role>`\n\n"
                msg += "**Example:** `" + prefix + "choose Innocent`\nThe options are **Innocent**, **Cursed Civilian** and **Werewolf**. "
                msg += "This command can only be used by the dog during the first night."

            '''execute'''
            # This command allows the executioner to choose a replacement target.
            if is_command(message,['choose','execute']) and user_role == "Executioner":
                # TODO
                return todo()
            if is_command(message,['choose','execute'],True) and user_role == "Executioner":
                msg = "**Usage:** Choose a victim to die instead of you on the lynch.\n\n`" + prefix + "execute <player>`\n\n"
                msg += "**Example:** `" + prefix + "execute @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by executioners it can be used for an unlimited amount of times."

            '''undoom'''
            # The Exorcist's command.
            if is_command(message,['exercise','exorcise','undoom']) and user_role == "Exorcist":
                # TODO
                return todo()
            if is_command(message,['exercise','exorcise','undoom'],True) and user_role == "Exorcist":
                msg = "**Usage:** Undoom a player.\n\n`" + prefix + "undoom <player>`\n\n"
                msg += "**Example:** `" + prefix + "undoom @Randium#6521`\nThe command is compatible with user emojis as a replacement for mentions. "
                msg += "This command can only be used by ."

            '''inspect'''
            # The fortune teller's command.
            if is_command(message,['forsee','inspect','see','tell']) and user_role == "Fortune Teller":
                # TODO
                return todo()
            if is_command(message,['forsee','inspect','see','tell'],True) and user_role == "Fortune Teller":
                # TODO
                return todo()

            '''silence'''
            # Grandma's command.
            if is_command(message,['knit','knot','silence']) and user_role == "Grandma":
                # TODO
                return todo()
            if is_command(message,['knit','knot','silence'],True) and user_role == "Grandma":
                # TODO
                return todo()

            '''hook'''
            # The hooker's command
            if is_command(message,['fuck','hook','sleep']) and user_role == "Hooker":
                # TODO
                return todo()
            if is_command(message,['fuck','hook','sleep'],True) and user_role == "Hooker":
                # TODO
                return todo()

            '''hunt'''
            # The huntress' command. Used to keep track of whom will be shot.
            if is_command(message,['hunt','shoot']) and user_role == "Huntress":
                # TODO
                return todo()
            if is_command(message,['hunt','shoot'],True) and user_role == "Huntress":
                # TODO
                return todo()

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

            '''copy'''
            # The Look-Alike's command
            if is_command(message,['copy','imitate','mirror','resemble']) and user_role == "Look-Alike":
                # TODO
                return todo()
            if is_command(message,['copy','imitate','mirror','resemble'],True) and user_role == "Look-Alike":
                # TODO
                return todo()

            '''holify'''
            # The Priest's command
            if is_command(message,['holify','sacrify','water']) and user_role == "Priest":
                # TODO
                return todo()
            if is_command(message,['holify','sacrify','water'],True) and user_role == "Priest":
                # TODO
                return todo()

            '''purify'''
            # The Priestess' command
            if is_command(message,['heal','light','purify','sacrify']) and user_role == "Priestess":
                # TODO
                return todo()
            if is_command(message,['heal','light','purify','sacrify'],True) and user_role == "Priestess":
                # TODO
                return todo()

            '''threaten'''
            # The Raven's command
            if is_command(message,['threaten','raven']) and user_role == "Raven":
                # TODO
                return todo()
            if is_command(message,['threaten','raven'],True) and user_role == "Raven":
                # TODO
                return todo()

            '''reveal'''
            # The Royal Knight's command
            if is_command(message,['end','prevent','reveal','stop']) and user_role == "Royal Knight":
                # TODO
                return todo()
            if is_command(message,['end','prevent','reveal','stop'],True) and user_role == "Royal Knight":
                # TODO
                return todo()

            '''life'''
            # The witch' command to use her life potion
            if is_command(message,['heal','life','save']) and user_role == "Witch":
                # TODO
                return todo()
            if is_command(message,['heal','life','save'],True) and user_role == "Witch":
                # TODO
                return todo()

            '''death'''
            # The witch' command to use her death potion
            if is_command(message,['death','kill','murder','poison']) and user_role == "Witch":
                # TODO
                return todo()
            if is_command(message,['death','kill','murder','poison'],True) and user_role == "Witch":
                # TODO
                return todo()

            '''çurse'''
            # The curse caster's command
            if is_command(message,['cast','corrupt','curse']) and user_role == "Curse Caster":
                # TODO
                return todo()
            if is_command(message,['cast','corrupt','curse'],True) and user_role == "Curse Caster":
                # TODO
                return todo()

            '''infect'''
            # The infected wolf's command
            if is_command(message,['cough','infect','sneeze','turn']) and user_role == "Infected Wolf":
                # TODO
                return todo()
            if is_command(message,['cough','infect','sneeze','turn'],True) and user_role == "Infected Wolf":
                # TODO
                return todo()

            '''devour'''
            # The Lone wolf's command
            if is_command(message,['chew','devour','eat','kill','munch']) and user_role == "Lone Wolf":
                # TODO
                return todo()
            if is_command(message,['chew','devour','eat','kill','munch'],True) and user_role == "Lone Wolf":
                # TODO
                return todo()

            '''disguise'''
            # The tanner's command
            if is_command(message,['change','cloth','disguise','hide']) and user_role == "Tanner":
                # TODO
                return todo()
            if is_command(message,['change','cloth','disguise','hide'],True) and user_role == "Tanner":
                # TODO
                return todo()

            '''inspect'''
            # The Warlock's command
            if is_command(message,['forsee','inspect','see','tell']) and user_role == "Priestess":
                # TODO
                return todo()
            if is_command(message,['forsee','inspect','see','tell'],True) and user_role == "Priestess":
                # TODO
                return todo()

            '''devour'''
            # The white werewolf's command
            if is_command(message,['chew','devour','eat','kill','munch']) and user_role == "White Werewolf":
                # TODO
                return todo()
            if is_command(message,['chew','devour','eat','kill','munch'],True) and user_role == "White Werewolf":
                # TODO
                return todo()

            '''wager'''
            # The devil's command
            if is_command(message,['choose','wager']) and user_role == "Devil":
                # TODO
                return todo()
            if is_command(message,['choose','wager'],True) and user_role == "Devil":
                # TODO
                return todo()

            '''enchant'''
            # The flute player's command
            if is_command(message,['enchant','flute']) and user_role == "Flute Player":
                # TODO
                return todo()
            if is_command(message,['enchant','flute'],True) and user_role == "Flute Player":
                # TODO
                return todo()

            '''unite'''
            # The horseman's command
            if is_command(message,['apocalypse','clean','unite']) and user_role == "Horseman":
                # TODO
                return todo()
            if is_command(message,['apocalypse','clean','unite'],True) and user_role == "Horseman":
                # TODO
                return todo()

            '''guess'''
            # The ice king's command to add a guess about a user to their list.
            # Note that this command could/should be usable at any time, as long as the submit command isn't
            if is_command(message,['add','guess','freeze']) and user_role == "Ice King":
                # TODO
                return todo()
            if is_command(message,['add','guess','freeze'],True) and user_role == "Ice King":
                # TODO
                return todo()

            '''submit'''
            # The ice king's command to submit the list of people of whom they have guessed their roles.
            if is_command(message,['guess_that','freeze_all','submit']) and user_role == "Ice King":
                # TODO
                return todo()
            if is_command(message,['guess_that','freeze_all','submit'],True) and user_role == "Ice King":
                # TODO
                return todo()

            '''powder'''
            # Powder a player
            if is_command(message,['creeper','powder']) and user_role == "Pyromancer":
                # TODO
                return todo()
            if is_command(message,['creeper','powder'],True) and user_role == "Pyromancer":
                # TODO
                return todo()

            '''abduct'''
            # To kidnap players
            if is_command(message,['abduct','add','kidnap','swamp']) and user_role == "The Thing":
                # TODO
                return todo()
            if is_command(message,['abduct','add','kidnap','swamp'],True) and user_role == "The Thing":
                # TODO
                return todo()

            '''create_swamp'''
            # To create a new swamp with all victims
            if is_command(message,['abduct_all','create_swamp','start_cliche_horror_movie']) and user_role == "The Thing":
                # TODO
                return todo()
            if is_command(message,['abduct_all','create_swamp','start_cliche_horror_movie'],True) and user_role == "The Thing":
                # TODO
                return todo()

    # =============================================================
    #
    #                         EVERYONE
    #
    # =============================================================

    '''age'''
    # Allows users to set their age.
    if is_command(message,['age']):
        # TODO
        return todo()
    if is_command(message,['age'],True):
        # TODO
        return todo()

    '''profile'''
    # This command allows one to view their own profile
    # When giving another player's name, view that player's profile
    if is_command(message,['profile']):
        # TODO
        return todo()
    if is_command(message,['profile'],True):
        # TODO
        return todo()

    '''signup'''
    # This command signs up the player with their given emoji, assuming there is no game going on.
    if is_command(message,['signup']):
        emojis = check.emojis(message)
        choice_emoji = ""

        if emojis == False:
            msg = "**Incorrect syntax:** `" + prefix + "signup <emoji>`\n\nExample: `" + prefix + "signup :smirk:`"
            return [Mailbox().respond(msg,True)]

        for emoji in emojis:
            if emoji_to_player(emoji) == None:
                choice_emoji = emoji
                break

        if isParticipant(user_id,True,True):
            if choice_emoji == "":
               return [Mailbox().respond("You are already signed up with the {} emoji! Also, your emoji was occupied.".format(db_get(user_id,'emoji')),True)]
            db_set(user_id,'emoji',choice_emoji)
            reaction = Mailbox().respond("You have successfully changed your emoji to the {} emoji!".format(choice_emoji))
            return [reaction.spam("<@{}> has changed their emoji to the {} emoji.".format(user_id,choice_emoji))]

        if choice_emoji == "":
            if len(choice_emoji) == 1:
                return [Mailbox().respond("I am sorry! Your chosen emoji was already occupied.",True)]
            return [Mailbox().respond("I am sorry, but all of your given emojis were already occupied! Such bad luck.",True)]
        signup(user_id,message.author.name,choice_emoji)
        reaction = Mailbox().respond("You have successfully signed up with the {} emoji!".format(choice_emoji))
        return [reaction.spam("<@{}> has signed up with the {} emoji.".format(user_id,choice_emoji))]
    # Help command
    if is_command(message,['signup'],True):
        msg = "**Usage:** `" + prefix + "signup <emoji>`\n\nExample: `" + prefix + "signup :smirk:`"
        return [Mailbox().respond(msg,True)]

    if message.content.startswith(prefix):
        return [Mailbox().respond("Sorry bud, couldn't find what you were looking for.",True)]

    return []

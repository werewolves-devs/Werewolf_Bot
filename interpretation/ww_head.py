# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from management.db import isParticipant, personal_channel, db_get, db_set, signup, emoji_to_player, channel_get, is_owner
from roles_n_rules.commands import cc_goodbye
from interpretation.check import is_command
from config import prefix, max_cc_per_user
from main_classes import Mailbox, Message
from discord import Embed
import roles_n_rules.functions as func
import interpretation.check as check
import discord

def todo():
    return [Mailbox().spam("I am terribly sorry! This command doesn't exist yet!",True)]

def process(message, isGameMaster = False):

    user_id = message.author.id
    message_channel = message.channel.id
    user_role = db_get(user_id,'role')

    '''testcc'''
    # This function is merely a temporary one, to test if the cc creation command is working properly.
    if is_command(message,['cc','testcc','test_cc']):
        members = check.users(message)
        if len(message.content.split(' ')) == 1 or members == False:
            msg = "**Incorrect syntax:** `" + prefix + "cc <name> <user> <user> <user> ...`\n\nExample: `" + prefix + "cc the_cool_ones @Randium#6521`"
            msg += "\n\nThe bot understands both mentions and emojis linked to players."
            return [Mailbox().respond(msg,True)]
        name = message.content.split(' ')[1]
        return [Mailbox().create_cc(name,user_id,members)]
    if is_command(message,['cc','testcc','test_cc'],True):
        msg = "**Usage:** `" + prefix + "cc <name> <user> <user> <user> ...`\n\nExample: `" + prefix + "cc the_cool_ones @Randium#6521`"
        msg += "\n\nThe bot understands both mentions and emojis linked to players."
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
            # TODO
            return todo()

        '''assign'''
        # This command is used at the start of the game to assign all roles.
        # This will actually set their "fakerole" value, which will be transferred to their actual role once the game starts.
        if is_command(message,['assign']):
            role = check.roles(message,1)[0]
            user = check.users(message,1)[0]

            if role == False:
                return [Mailbox().respond("No role provided! Please provide us with a role!")]
            if user == False:
                return [Mailbox().respond("No user found! Please provide us with a user!")]

            db_set(user,'role',role)
            return [Mailbox().spam("You have successfully given <@{}> the role of the `{}`!".format(user,role))]

        if is_command(message,['assign'],True):
            msg = "**Usage:** `" + prefix + "assign <user> <role>`\n\nExample: `" + prefix
            msg += "assign @Randium#6521 Innocent`\nGame Master only command"
            return [Mailbox().spam(msg)]

        '''day'''
        # This command is used to initialize the day.
        if is_command(message,['day']):
            # TODO
            return todo()
        if is_command(message,['day'],True):
            # TODO
            return todo()

        '''open_signup'''
        # This command is started when a new game can be started.
        # Make sure the bot has reset itself beforehand.
        if is_command(message,['open_signup']):
            # TODO
            return todo()
        if is_command(message,['open_signup'],True):
            # TODO
            return todo()

        '''whois'''
        # This command reveals the role of a player.
        # To prevent spoilers, the response isn't made in the message's channel, but rather in the bot spam channel.
        if is_command(message,['whois']):
            user_table = check.users(message)
            identities = Mailbox()

            if user_table == False:
                return [Mailbox().respond("**ERROR:** No user provided!")]

            for user in user_table:
                emoji = db_get(user,'emoji')
                role = db_get(user,'role')
                if emoji == None or role == None:
                    identities.spam("**ERROR:** Could not find user <@{}> in database.".format(user))
                else:
                    msg = "{} - <@{}> has the role of the `{}`!".format(emoji,user,role)
                    identities.spam(msg)

            return [identities]

        if is_command(message,['whois'],True):
            msg = "**Usage:** `" + prefix + "whois <user1> <user2> ...`\n\n"
            msg += "Example: `" + prefix + "whois @Randium#6521`\nGame Master only command"
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
                if int(db_get(member,'abducted')) == 1:
                    command.edit_cc(message_channel,member,3)
                elif int(db_get(member,'frozen')) == 1:
                    command.edit_cc(message_channel,member,2)
                elif isParticipant(member):
                    command.edit_cc(message_channel,member,1)
                else:
                    command.edit_cc(message_channel,member,4)
            return [command.respond("Changes saved! I will execute these now.")]

        if is_command(message,['add'],True):
            # TODO
            return todo()

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
                return answer.dm("If you want more conspiracy channels, please request permission from one of the Game Masters.", user_id)

            db_set(user_id,'ccs',num_cc_owned + 1)
            return Mailbox.create_cc(message.content.split(' ')[1], user_id, channel_members)

        if is_command(message,['cc'],True):
            # TODO
            return todo()

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

            embed.add_field(name='Channel Name', value=message.channel.name)
            embed.add_field(name='Participants', value='[Bob Roberts], [Dummy], [Randium], [BenTechy66], [Ed588]')
            embed.set_footer(text='Conspiracy Channel Information requested by ' + message.author.nick)
            return [Mailbox().embed(embed, message.channel.id)]
        if is_command(message,['info'],True):
            # TODO
            return todo()

        '''myrole'''
        # This command sends the user's role back to them in a DM.
        if is_command(message,['myrole']):
            return [Mailbox().dm("Your role is **{}**.".format(db_get(message.author.id,'role')), message.author.id,False,[db_get(message.author.id,'emoji')])]
        if is_command(message,['myrole'],True):
            # TODO
            return todo()

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
            # TODO
            return todo()

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
                return [Mailbox().respond("")]

            '''aura'''
            # The command for aura tellers
            if is_command(message,['aura','tell','vision']) and user_role == "Aura Teller":
                # TODO
                return todo()
            if is_command(message,['aura','tell','vision'],True) and user_role == "Aura Teller":
                # TODO
                return todo()

            '''barber_kill'''
            # Barber kill - to assassinate a victim during the day
            if is_command(message,['assassinate','barber_kill','cut']) and user_role == "Barber":
                # TODO
                return todo()
            if is_command(message,['assassinate','barber_kill','cut'],True) and user_role == "Barber":
                # TODO
                return todo()

            '''seek'''
            # Crowd seeker's power
            if is_command(message,['crowd','seek']) and user_role == "Crowd Seeker":
                # TODO
                return todo()
            if is_command(message,['crowd','seek'],True) and user_role == "Crowd Seeker":
                # TODO
                return todo()

            '''kiss'''
            # Cupid's power to fall in love with someone.
            if is_command(message,['kiss','love','shoot']) and user_role == "Cupid":
                # TODO
                return todo()
            if is_command(message,['kiss','love','shoot'],True) and user_role == "Cupid":
                # TODO
                return todo()

            '''follow'''
            # The command that allows the dog to choose a side.
            if is_command(message,['bark','become','choose','follow']) and user_role == "Dog":
                # TODO
                return todo()
            if is_command(message,['bark','become','choose','follow'],True) and user_role == "Dog":
                # TODO
                return todo()

            '''execute'''
            # This command allows the executioner to choose a replacement target.
            if is_command(message,['choose','execute']) and user_role == "Executioner":
                # TODO
                return todo()
            if is_command(message,['choose','execute'],True) and user_role == "Executioner":
                # TODO
                return todo()

            '''undoom'''
            # The Exorcist's command.
            if is_command(message,['exercise','exorcise','undoom']) and user_role == "Exorcist":
                # TODO
                return todo()
            if is_command(message,['exercise','exorcise','undoom'],True) and user_role == "Exorcist":
                # TODO
                return todo()

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
                # TODO
                return todo()
            if is_command(message,['melt','unfreeze'],True) and user_role == "Innkeeper":
                # TODO
                return todo()

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

        if emoji == "":
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

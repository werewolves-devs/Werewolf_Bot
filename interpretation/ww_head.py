# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from management.db import isParticipant, personal_channel, db_get, db_set
from check import is_command
import roles_n_rules.functions as func
from main_classes import Mailbox
from config import prefix
import check

def todo():
    return [Mailbox().spam("I am terribly sorry! This command doesn't exist yet!",True)]

def process(message, isGameMaster = False):

    user_id = message.author.id
    message_channel = message.channel
    user_role = db_get(user_id,'role')

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

            for user in user_table:
                emoji = db_get(user,'emoji')
                role = db_get(user,'role')
                msg = "{} - <@{}> has the role of the `{}`!".format(emoji,user,role)
                identities.spam(msg)
            
            return [identities]

        if is_command(message,['whois'],True):
            msg = "**Usage:** `" + prefix + "whois <user1> <user2> ...`\n\n"
            msg += "Example: `" + prefix + "whois @Randium#6521`\nGame Master only command" 

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
            # TODO
            return todo()
        if is_command(message,['add'],True):
            # TODO
            return todo()

        '''cc'''
        # This command allows users to create a conspirachy channel.
        if is_command(message,['cc']):
            # TODO
            return todo()
        if is_command(message,['cc'],True):
            # TODO
            return todo()

        '''info'''
        # This command allows users to view information about a conspiracy channel.
        # Says the user must be in a cc if they're not.
        if is_command(message,['info']):
            # TODO
            return todo()
        if is_command(message,['info'],True):
            # TODO
            return todo()

        '''myrole'''
        # This command sends the user's role back to them in a DM.
        if is_command(message,['myrole']):
            # TODO
            return todo()
        if is_command(message,['myrole'],True):
            # TODO
            return todo()
        
        '''remove'''
        # This command removes a given user from a conspiracy channel.
        # A user should not get removed if they're the channel owner.
        if is_command(message,['remove']):
            # TODO
            return todo()
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
                # TODO
                return todo()
            if is_command(message,['assassinate','kill'],True) and user_role == "Assassin":
                # TODO
                return todo()
            
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
        # TODO
        return todo()
    if is_command(message,['signup'],True):
        # TODO
        return todo()

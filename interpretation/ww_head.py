# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
from management.db import isParticipant, personal_channel, db_get, db_set
from check import is_command
import roles_n_rules.functions as func
from main_classes import Mailbox
from config import prefix
import check

def todo():
    return [Mailbox().msg("I am terribly sorry! This command doesn't exist yet!","",True)]

def process(message, isGameMaster = False):

    user_id = message.author.id
    message_channel = message.channel
    role = db_get(user_id,'role')

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
            role = check.roles(message,1)
            user = check.users(message,1)

            db_set(user,'role',role)
            return Mailbox().spam("You have successfully given <@{}> the role of the `{}`!".format(user,role))

        if is_command(message,['assign'],True):
            # TODO
            return todo()
        
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
        # To prevent spoilers, the response isn't made in the message's channel, but rather in the bot spam channel,
        # including a mention of the Game Master to attend them the message didn't fail.
        if is_command(message,['whois']):
            # TODO
            return todo()
        if is_command(message,['whois'],True):
            # TODO
            return todo()

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
            if is_command(message,['assassinate','kill']):
                # TODO
                return todo()
            if is_command(message,['assassinate','kill'],True):
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

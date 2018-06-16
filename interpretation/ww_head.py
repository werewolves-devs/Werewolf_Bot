# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
import roles_n_rules.functions as func
from main_classes import Mailbox
from config import prefix

def todo():
    return [Mailbox().msg("I am terribly sorry! This command doesn't exist yet!","",True)]

def process(message, isGameMaster = False):

    user_id = message.author.id
    message_channel = message.channel

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
        if message.content.startswith(prefix + 'addrole'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help addrole'):
            # TODO
            return todo()

        '''assign'''
        # This command is used at the start of the game to assign all roles.
        # This will actually set their "fakerole" value, which will be transferred to their actual role once the game starts.
        if message.content.startswith(prefix + 'assign'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help assign'):
            # TODO
            return todo()
        
        '''open_signup'''
        # This command is started when a new game can be started.
        # Make sure the bot has reset itself beforehand.
        if message.content.startswith(prefix + 'open_signup'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help open_signup'):
            # TODO
            return todo()

        '''whois'''
        # This command reveals the role of a player.
        # To prevent spoilers, the response isn't made in the message's channel, but rather in the bot spam channel,
        # including a mention of the Game Master to attend them the message didn't fail.
        if message.content.startswith(prefix + 'whois'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help whois'):
            # TODO
            return todo()

    # =============================================================
    #
    #                         PARTICIPANTS
    #
    # =============================================================

    if False: #TODO: check if user is a participant

        '''add'''
        # This command allows users to add users to a conspiracy.
        # This command will not trigger if the user doesn't own the conspiracy channel.
        if message.content.startswith(prefix + 'add'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help add'):
            # TODO
            return todo()

        '''cc'''
        # This command allows users to create a conspirachy channel.
        if message.content.startswith(prefix + 'cc'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help cc'):
            # TODO
            return todo()

        '''info'''
        # This command allows users to view information about a conspiracy channel.
        # Says the user must be in a cc if they're not.
        if message.content.startswith(prefix + 'info'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help info'):
            # TODO
            return todo()

        '''myrole'''
        # This command sends the user's role back to them in a DM.
        if message.content.startswith(prefix + 'myrole'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help myrole'):
            # TODO
            return todo()
        
        '''remove'''
        # This command removes a given user from a conspiracy channel.
        # A user should not get removed if they're the channel owner.
        if message.content.startswith(prefix + 'remove'):
            # TODO
            return todo()
        if message.content.startswith(prefix + 'help remove')
            # TODO
            return todo()

    # =============================================================
    #
    #                         EVERYONE
    #
    # =============================================================

    '''age'''
    # Allows users to set their age.
    if message.content.startswith(prefix + 'age'):
        # TODO
        return todo()
    if message.content.startswith(prefix + 'help age'):
        # TODO
        return todo()

    '''profile'''
    # This command allows one to view their own profile
    # When giving another player's name, view that player's profile
    if message.content.startswith(prefix + 'profile'):
        # TODO
        return todo()
    if message.content.startswith(prefix + 'help profile'):
        # TODO
        return todo()

    '''signup'''
    # This command signs up the player with their given emoji, assuming there is no game going on.
    if message.content.startswith(prefix + 'signup'):
        # TODO
        return todo()
    if message.content.startswith(prefix + 'help signup'):
        # TODO
        return todo()

# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
import roles_n_rules.functions as func
from config import prefix

def todo():
    raise SyntaxError("This command isn't finished yet!")

def process(message, isGameMaster = False):

    user_id = message.author.id
    message_channel = message.channel

    # =============================================================
    #
    #                         GAME MASTERS
    #
    # =============================================================
    if isGameMaster == True:

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

    '''myrole'''
    # This command sends the user's role back to them in a DM
    if message.content.startswith(prefix + 'myrole'):
        # TODO
        return todo()
    if message.content.startswith(prefix + 'help myrole'):
        # TODO
        return todo()

    # =============================================================
    #
    #                         EVERYONE
    #
    # =============================================================

    '''signup'''
    # This command signs up the player with their given emoji, assuming there is no game going on.
    if message.content.startswith(prefix + 'signup'):
        # TODO
        return todo()
    if message.content.startswith(prefix + 'help signup'):
        # TODO
        return todo()

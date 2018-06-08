# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
import roles_n_rules.functions as func
from config import prefix

def todo():
    raise SyntaxError("This command isn't finished yet!")

def process(message, isGameMaster = False):

    user_id = message.author.id
    message_channel = message.channel

    '''myrole'''
    # This command sends the user's role back to them in a DM
    if message.content.startswith(prefix + 'myrole'):
        # TODO
        return todo()
    if message.content.startswith(prefix + 'help myrole'):
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

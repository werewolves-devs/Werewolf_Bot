# This is the main file that cuts the message into pieces and transfers the info the the map roles_n_rules.
import roles_n_rules.functions as func
from config import prefix

def todo():
    print "This command isn't finished yet!"
    raise SyntaxError()

def process(message):

    user_id = message.author.id
    message_channel = message.channel

    # This command sends the user's role back to them in a DM
    if message.content.startswith(prefix + 'myrole'):
        # TODO
        return False
    if message.content.startswith(prefix + 'help myrole'):
        # TODO
        return False
    

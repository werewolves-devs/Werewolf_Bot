''' These are the functions that yet need to be made.

myrole()
kill_queue()

signup()

syntax_signup()

'''
import management.db as db
from main_classes import Mailbox

def signup(user_id,emoji,channel):
    if db.emoji_to_player(emoji) != None:
        mail = Mailbox().respond("I am terribly sorry! That emoji has already been taken!",channel)

def syntax_signup():
    pass

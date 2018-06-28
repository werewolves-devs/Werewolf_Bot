''' These are the functions that yet need to be made.

myrole()
kill_queue()

signup()

syntax_signup()

'''
import management.db as db
from main_classes import Mailbox

def myrole():
    return db.db_get(message.author.id,'role')

def signup(user_id,emoji,channel):
    if db.emoji_to_player(emoji) != None:
        mail = Mailbox().respond("I am terribly sorry! That emoji has already been taken!",channel)

def syntax_signup():
    pass

def suicide(user_id):
    if db.db_get(user_id,'role') in ["Spectator", "Dead"]:
        return Mailbox().respond("Sorry, but this player cannot be killed again once they are dead!")
    else:
        db_set(user_id,'role','Dead')
        return Mailbox().respond("<@{}> has been killed.".format(user_id))


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

def suicide():
    if player.role.name in ["Spectator", "Dead"]:
        return mail = Mailbox().respond("Sorry, but you cannot kill yourself once you are dead!",me.channel)
    else:
        db_set(user_id,'role','Dead')
        return mail = Mailbox().respond("Seeing that you cannot do or acheive anymore, clearly life was not worth living anymore and you have committed suicide. The town, upon closer investigation, has found out that " + player.name + " was a " + db_get(user_id,'role') + ".")


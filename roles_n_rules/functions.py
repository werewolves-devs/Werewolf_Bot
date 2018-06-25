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
    if player.role.name in ["Spectator", "Dead"] or me.dead == True:
        return mail = Mailbox().respond("Sorry, but you cannot kill yourself once you are dead!",me.channel)
    else:
        me.dead = True
        player.role.name in ["Dead"]
        return mail = Mailbox().respond("You have committed suicide, upon closer investigate, it has been found out that " + player.name + " was a " + player.role.name + ".")


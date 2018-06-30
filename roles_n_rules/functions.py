''' These are the functions that yet need to be made.

myrole()
kill_queue()

signup()

syntax_signup()

'''
import management.db as db
import discord
from main_classes import Mailbox
from config import game_master

def myrole(user_id=message.author.id, message):
    if game_master in [y.id for y in message.author.roles]:
        return Mailbox().respond("The role of user <@{}> is {}".format(user_id, db.db_get(user_id,'role')).dm()
    elif game_master not in [y.id for y in message.author.roles] and user_id != message.author.id:
        return Mailbox().respond("Hey stop that! You're not a game master! No peeking at anyone else's roles!").dm()
    else:
        return Mailbox().respond("Your role is {}".format(db.db_get(message.author.id,'role')).dm()
    

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


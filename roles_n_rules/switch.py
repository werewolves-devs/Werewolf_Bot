from management import db, dynamic as dy, setup
from management.db import db_get, db_set, channel_change_all
from management.setup import view_roles

def cc_freeze(user_id):
    db_set(user_id,'frozen',1)
    answer = Mailbox().spam("<@{}> was frozen.".format(user_id))

    for channel in channel_change_all(user_id,1,2):
        answer.edit_cc(channel,user_id,2)
    return answer

def cc_unfreeze(user_id):
    db_set(user_id,'frozen',0)
    answer = Mailbox().spam("<@{}> is no longer frozen.".format(user_id))

    for channel in channel_change_all(user_id,2,1):
        answer.edit_cc(channel,user_id,1)
    return answer

def cc_abduct(user_id):
    db_set(user_id,'abducted',1)
    answer = Mailbox().spam("<@{}> has been abducted.".format(user_id))

    for channel in channel_change_all(user_id,1,3):
        answer.edit_cc(channel,user_id,3)
    for channel in channel_change_all(user_id,5,6):
        answer.edit_cc(channel,user_id,6)
    return answer

def cc_unabduct(user_id):
    db_set(user_id,'abducted',0)
    answer = Mailbox().spam("<@{}> is no longer abducted.".format(user_id))

    for channel in channel_change_all(user_id,3,1):
        answer.edit_cc(channel,user_id,1)
    for channel in channel_change_all(user_id,6,5):
        answer.edit_cc(channel,user_id,5)
    for channel in channel_change_all(user_id,7,4):
        answer.edit_cc(channel,user_id,4)

def cc_suspend(user_id):
    answer = Mailbox().spam("<@{}> has been suspended.".format(user_id))

    for channel in channel_change_all(user_id,1,8):
        answer.edit_cc(channel,user_id,8)
    for channel in channel_change_all(user_id,2,8):
        answer.edit_cc(channel,user_id,8)
    for channel in channel_change_all(user_id,3,8):
        answer.edit_cc(channel,user_id,8)
    for channel in channel_change_all(user_id,4,8):
        answer.edit_cc(channel,user_id,8)
    for channel in channel_change_all(user_id,5,8):
        answer.edit_cc(channel,user_id,8)
    for channel in channel_change_all(user_id,6,8):
        answer.edit_cc(channel,user_id,8)
    for channel in channel_change_all(user_id,7,8):
        answer.edit_cc(channel,user_id,8)
    return answer

def pay():
    """This function takes care of all properties that need to happen in the first wave of the end of the night.
    The function returns a Mailbox."""

    answer = Mailbox(True)
    for user in db.player_list():
        user_role = db_get(user,'role')

        # Remove tanner disguises
        db_set(user,'fakerole',user_role)

def start_game():
    """This function is triggered at the start of the game. If successful, the function returns a Mailbox.
    If unsuccessful, the function still returns a Mailbox, but will also confirm the error in the console."""

    # Make sure there isn't already a game going on!
    if dy.get_stage() != "NA":
        print("ERROR: According to " + dy.dynamic_config + ", there's already a game going on!")
        return Mailbox().respond("I'm sorry! A game cannot be started while there's another one going on already!")

    # Choose the roles out of the given role-pool
    role-pool = []
    for choice in view_roles:
        for i in range(choice.amount):
            role-pool.append(choice.role)

    if len(db.player_list) > len(role-pool):
        print("The game cannot be started while there are less roles available than that there are participants signed up.")
        return Mailbox()

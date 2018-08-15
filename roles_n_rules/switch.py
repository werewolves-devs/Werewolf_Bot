from main_classes import Mailbox
from management import db, dynamic as dy, setup
from management.db import db_get, db_set, channel_change_all
from management.setup import view_roles
from roles_n_rules.functions import cupid_kiss
import random
import roles_n_rules.role_data as roles

def pay():
    """This function takes care of all properties that need to happen in the first wave of the end of the night.
    The function returns a Mailbox."""

    answer = [Mailbox(True)]
    for user_id in db.player_list():
        user_role = db_get(user_id,'role')
        dy.next_day()

        # Remove potential night uses
        for i in range(len(roles.night_users)):
            if user_role in roles.night_users[i]:
                if i > 0:
                    db_set(user_id,'uses',0)
                break

        # Give potential day uses
        for i in range(len(roles.day_users)):
            if user_role in roles.day_users[i]:
                # Give one-time users their one-time power
                if i == 0:
                    if dy.day_number() == 0:
                        db_set(user_id,'uses',1)
                    break
                
                db_set(user_id,'uses',i)
                break

        # Force Cupid to fall in love
        if user_role == "Cupid" and db_get(user_id,'uses') > 0:
            chosen = False
            attempts = 0

            while not chosen and attempts < 100:
                forced_victim = random.choice(db.player_list(True,True))
                chosen = cupid_kiss(user_id,forced_victim,False)
            
            answer.append(chosen)

        # Force Dog to become Innocent
        if user_role == "Dog":
            db_set(user_id,'role',"Innocent")
            response = Mailbox().msg("You haven't chosen a role! That's why you have now become and **Innocent**!",db_get(user_id,'channel'))
            response.log("The **Dog** <@{}> didn't choose a role last night and turned into an **Innocent**!".format(user_id))
            answer.append(response)

        # Remove hooker effects
        db_set(user_id,'sleepingover',0)
        for standoff in db.get_standoff(user_id):
            if standoff[2] == 'Hooker':
                db.delete_standoff(standoff[0])

        # Force Look-Alike to become Innocent
        if user_role == "Look-Alike":
            db_set(user_id,'role',"Innocent")
            response = Mailbox().msg("You haven't chosen a role! That's why you have now become and **Innocent**!",db_get(user_id,'channel'))
            response.log("The **Dog** <@{}> didn't choose a role last night and turned into an **Innocent**!".format(user_id))
            answer.append(response)

        # Remove tanner disguises
        db_set(user_id,'fakerole',user_role)

def start_game():
    """This function is triggered at the start of the game. If successful, the function returns a Mailbox.
    If unsuccessful, the function still returns a Mailbox, but will also confirm the error in the console."""

    # Make sure there isn't already a game going on!
    if dy.get_stage() != "NA":
        print("ERROR: According to " + dy.dynamic_config + ", there's already a game going on!")
        return Mailbox().respond("I'm sorry! A game cannot be started while there's another one going on already!")

    # Choose the roles out of the given role-pool
    role_pool = []
    for choice in view_roles():
        for i in range(choice.amount):
            role_pool.append(choice.role)

    if len(db.player_list) > len(role_pool):
        print("The game cannot be started while there are less roles available than that there are participants signed up.")
        return Mailbox()

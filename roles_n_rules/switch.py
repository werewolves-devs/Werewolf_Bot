from main_classes import Mailbox
from management import db, dynamic as dy, setup, position as pos
from management.db import db_get, db_set, channel_change_all
from management.setup import view_roles
from roles_n_rules.functions import cupid_kiss
import random
import roles_n_rules.role_data as roles
import story_time.powerup as power
import story_time.morning as morning
import config

def pay():
    """This function takes care of all properties that need to happen in the first wave of the end of the night.
    The function returns a Mailbox."""

    answer_table = []
    answer = Mailbox(True)
    for user_id in db.player_list():
        user_role = db_get(user_id,'role')

        # Remove potential night uses
        for i in range(len(roles.night_users)):
            if user_role in roles.night_users[i]:
                if i > 0:
                    db_set(user_id,'uses',0)
                break

        # Force Cupid to fall in love
        if user_role == "Cupid" and db_get(user_id,'uses') > 0:
            chosen = False
            attempts = 0

            while not chosen and attempts < 1000:
                forced_victim = random.choice(db.player_list(True,True))
                chosen = cupid_kiss(user_id,forced_victim,False)
            
            answer_table.append(chosen)

        # Force Dog to become Innocent
        if user_role == "Dog" and db_get(user_id,'uses') > 0:
            db_set(user_id,'role',"Innocent")
            answer.msg("You haven't chosen a role! That's why you have now become and **Innocent**!",db_get(user_id,'channel'))
            answer.log("The **Dog** <@{}> didn't choose a role last night and turned into an **Innocent**!".format(user_id))

        # Remove hooker effects
        db_set(user_id,'sleepingover',0)
        for standoff in db.get_standoff(user_id):
            if standoff[2] == 'Hooker':
                db.delete_standoff(standoff[0])

        # Force Look-Alike to become Innocent
        if user_role == "Look-Alike":
            db_set(user_id,'role',"Innocent")
            answer.msg("You haven't chosen a role! That's why you have now become an **Innocent**!",db_get(user_id,'channel'))
            answer.log("The **Dog** <@{}> didn't choose a role last night and turned into an **Innocent**!".format(user_id))

        # Remove tanner disguises
        db_set(user_id,'fakerole',user_role)
        
        # Remove zombie tag
        db_set(user_id,'bitten',0)

    return answer

def day():
    """Start the second part of the day.  
    The function assumes all polls have been evaluated, and that looking after attacks can begin.  
    The function returns a Mailbox."""
    threat = db.get_kill()
    answer = Mailbox()

    while threat != None:

        answer = roles.attack(threat[1],threat[2],threat[3],answer.log("**Results from night attacks:**\n"))
        threat = db.get_kill()
    
    for player in db.player_list(True):
        # Give potential day uses
        user_role = db_get(player,'role')
        for i in range(len(roles.day_users)):
            if user_role in roles.day_users[i]:
                # Give one-time users their one-time power
                if i == 0:
                    if dy.day_number() == 0:
                        db_set(user_id,'uses',1)
                    break
                
                db_set(player,'uses',i)
                answer.msg(power.power(user_role),db_get(player,'channel'))
                break
    
    answer.story(morning.story_time(db.get_deadies()))

    return answer

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

    if len(db.player_list()) > len(role_pool):
        print("The game cannot be started while there are less roles available than that there are participants signed up.")
        return Mailbox().respond("Not enough roles to distribute available!",True)
    
    # If there are enough roles available, make a selection, evaluate the selection, and, if accepted, distribute the roles.
    if not pos.valid_distribution(role_pool,True):
        return Mailbox().respond("I am sorry, but I cannot use an invalid distribution to start the game!",True)
    
    answer = Mailbox(True)

    attempts = 0
    while attempts < 1000:
        attempts += 1
        chosen_roles = random.sample(role_pool,len(db.player_list()))

        if pos.valid_distribution(chosen_roles,True) == True:


            # Assign the roles to all users.
            user_list = db.player_list()

            for i in range(len(user_list)):
                user_id = user_list[i]
                user_role = chosen_roles[i]

                db_set(user_id,'role',user_role)
                db_set(user_id,'fakerole',user_role)
                db_set(user_id,'channel',config.game_log)

                answer.dm("This message is giving you your role for season `{}` of the *Werewolves* game.\n\n".format(config.season),user_id)
                answer.dm_add('Your role is `{}`.\n\n'.format(user_role))
                answer.dm_add("**You are not allowed to share a screenshot of this message!** ")
                answer.dm_add("You can claim whatever you want about your role, but you may under **NO** ")
                answer.dm_add("circumstances show this message in any way to any other participants.\n")
                answer.dm_add("We hope you are happy with the role you gained, and we hope you'll enjoy the game as much as we do.\n\n")
                answer.dm_add("Good luck... 🌕")

                if user_role in pos.personal_secrets:
                    answer.create_sc(user_id,user_role)
                if user_role in pos.shared_secrets:
                    answer.add_to_sc(user_id,user_role)
                
                if user_role == "Cult Member":
                    answer.add_to_sc(user_id,"Cult Leader")
                if user_role in pos.wolf_pack:
                    answer.add_to_sc(user_id,"Werewolf")
                if user_role == "Bloody Butcher":
                    answer.add_to_sc(user_id,"Baker")
                if user_role == "Devil":
                    answer.add_to_sc(user_id,"Demon")
                if user_role == "Vampire":
                    answer.add_to_sc(user_id,"Undead")
                if user_role == "Witch":
                    db_set(user_id,'uses',3)
            
            # If the four horsemen are part of the game, assign numbers to all players.
            if "Horseman" in chosen_roles:
                nothorse_table = [user_id for user_id in db.player_list() if db_get(user_id,'role') != 'Horseman']
                horse_table = [user_id for user_id in db.player_list() if db_get(user_id,'role') == 'Horseman']

                nothorse_table.shuffle()
                horse_table.shuffle()

                for i in range(4):
                    db_set(horse_table[i],'horseman',i+1)

                for i in range(16):
                    db_set(nothorse_table[i],'horseman',(i%4)+1)
            
            # Reset the day timer
            dy.reset_day()
            dy.set_stage('Night')

            return answer
    
    answer.respond("Timeout reached! Your distribution is too crazy!",True)
    return answer
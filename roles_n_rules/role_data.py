night_users = [
    ["Cupid","Dog","Look-Alike"],
    ["Assassin","Aura Teller","Exorcist","Fortune Teller","Hooker","Innkeeper","Priest","Priestess","Raven","Curse Caster",
        "Infected Wolf","Lone Wolf","Warlock","Devil","Ice King","Pyromancer","The Thing","Vampire","Zombie"],
    [],
    ["Crowd Seeker","Grandma","Tanner"]
    ]

day_users = [[],["Barber","Royal Knight"],[],["Tanner"]]

import management.db as db
from management.db import db_get, db_set
from main_classes import Mailbox
from management.dynamic import lifepotion_in_play

def death():
    """What is death?  
    In this case it means emptying death-row. Let's see what you got in stock for us!"""

    answer = Mailbox()
    deadies = []
    if lifepotion_in_play():

        return answer.log("At the end of the night, no deaths were found due to the witch's life potion.")

    # [id,victim,role,murderer]
    order = db.get_kill()

    while order != None:

        victim_id = int(order[1])
        victim_role = db_get(victim_id,'role')
        role = order[2]
        murderer = order[3]

        if victim_role not in ['Dead','Spectator','Suspended',None,'Unknown']:
            # Standard day town kill
            if role in ["Innocent"]:
                # TODO
                pass

            # Standard night town kill
            if role in ["Assassin","Cult Leader","Witch"]:
                # TODO
                pass

            # Standard night wolf kill
            if role in ["Werewolf","Lone Wolf","White Werewolf"]:
                # TODO
                pass

            # Instant kill
            if role in ["Barber","Cupid","Executioner","Huntress","Devil","Zombie"]:
                # TODO
                pass

            # Add Priest test
            if role in ["Priest"]:
                # TODO
                pass
            
            # Devil's soul kill (not the wager!)
            if role in ["Demon"]:
                # TODO
                pass

            # Horseman kill
            if role in ["Horseman"]:
                # TODO
                pass

            # Pyromancer ignite
            if role in ["Pyromancer"]:
                if int(db_get(victim_id,'powdered')) == 1:
                    answer = death_by_night(answer,victim_id,role)

            # Abducted kill
            if role in ["The Thing"]:
                # TODO
                pass

            # Turn someone into a fortune teller
            if role in ["Fortune Teller",]:
                if int(db_get(victim_id,'undead')) == 1:
                    answer.msg("Your idol, the fortune teller <@{}>, has deceased. ".format(murderer),db_get(victim_id,'channel'))
                    answer.msg_add("They were a great inspiration to you... ")
                    answer.msg_add("back when you were alive, at least. Now, your undead heart is as cold as it has ever been, ")
                    answer.msg_add("and nothing will happen to you.\n")
                    answer.msg_add("**The rules have changed. You will remain Undead.**")

                    answer.log("Had <@{}> not been **Undead**, then <@{}>'s death would've turned them into a **Fortune Teller**.".format(victim_id,murderer))
                else:
                    answer.msg("Your idol, the fortune teller <@{}>, has deceased. ".format(murderer),db_get(victim_id,'channel'))
                    answer.msg_add("They were a great inspiration to you, and that's why ")
                    answer.msg_add("you've decided to get in their footsteps!\n")
                    answer.msg_add("**You have turned into a Fortune Teller. Find and ")
                    answer.msg_add("eliminate all werewolves, solo players and other enemies!**")

                    db_set(victim_id,'role','Fortune Teller')

                    answer.log("Due to <@{}>'s death, the **{}** <@{}> has turned into a **Fortune Teller**.".format(murderer,victim_role,victim_id))

        order = db.get_kill()
    
    return answer

def death_by_night(answer,user_id,role):
    """Kills a user during the night according to a standard procedure."""

    user_role = db_get(user_id,'role')

    if user_role in ['Sacred Wolf']:
        return answer.log('The **Sacred Wolf** <@{}> was protected from death.'.format(user_id))
    
    # Check if user has an amulet
    # TODO

    souls = db_get(user_id,'souls')
    if souls > 0:
        db_set(user_id,'souls',souls-1)
        answer.log('<@{}> lost a soul, but survived an attack.')
    
    # TODO

    return answer
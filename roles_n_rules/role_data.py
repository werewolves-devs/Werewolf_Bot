night_users = [
    ["Cupid","Dog","Look-Alike"],
    ["Assassin","Aura Teller","Exorcist","Fortune Teller","Hooker","Innkeeper","Priest","Priestess","Raven","Curse Caster",
        "Infected Wolf","Lone Wolf","Warlock","Devil","Ice King","Pyromancer","The Thing","Vampire","Zombie"],
    [],
    ["Crowd Seeker","Grandma","Tanner"]
    ]

day_users = [[],["Barber","Royal Knight"],[],["Tanner"]]

import management.position as pos
import management.db as db
from management.db import db_get, db_set
from main_classes import Mailbox
from management.dynamic import lifepotion_in_play
from story_time.barber_kills import barber_kill_story

def death():
    """What is death?  
    In this case it means emptying death-row. Let's see what you got in stock for us!"""

    answer = Mailbox()
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
                if victim_role == 'Cursed Civilian':
                    answer.dm("The curse that went around you, had been a little itchy lately... and it kept getting worse! ",victim_id)
                    answer.dm_add("It got worse and worse, and you couldn't help but notice how hair started growing everywhere!\n")
                    answer.dm_add("Last night, you were waking up by the grunts of a what sounded like a wolf! ")
                    answer.dm_add("You thought your days were over, but the wolf did not attack. Instead, ")
                    answer.dm_add("the wolf watched as your nails grew longer, your ears became spiky and your smell ")
                    answer.dm_add("slowly improved... and you looked just like one of the silhouettes in the shadow, ")
                    answer.dm_add("waiting for you to join them in the beautiful night's sky...\n")
                    answer.dm_add("**You have been visited by wolves last night, and your curse made you turn ")
                    answer.dm_add("into a werewolf. Devour all villagers and win the game!**")

                    db_set(victim_id,'role','Werewolf')
                    answer.log("The **Cursed Civilian** <@{}> has turned into a **Werewolf**!".format(victim_id))

                    for channel_id in db.get_secret_channels('Werewolf'):
                        answer.edit_cc(channel_id,victim_id,1)
                        answer.msg("**ARRROOOO!\nWelcome, <@{}>!**".format(victim_id),channel_id)
                        answer.msg_add("Last night, the **cursed civilian** <@{}> was attacked by wolves, ")
                        answer.msg_add("and has now become a **werewolf**! Please, welcome this new member ")
                        answer.msg_add("of the wolf pack!")
                else:
                    answer = death_by_night(answer,victim_id,role)

            # Instant kill
            if role in ["Barber","Cupid","Executioner","Huntress","Devil","Zombie","Macho"]:
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
                if role == "Horseman":
                    number = db_get(victim_id,'horseman')
                    for horsedude_id in db.player_list():
                        if db_get(horsedude_id,'horseman') == number:
                            db_set(horsedude_id,'horseman',0)

            # Pyromancer ignite
            if role in ["Pyromancer"]:
                if int(db_get(victim_id,'powdered')) == 1:
                    answer = death_by_night(answer,victim_id,role)

            # Abducted kill
            if role in ["The Thing"]:
                # TODO
                pass

            # Turn someone into an infected wolf
            if role in ["Infected Wolf"]:
                # TODO
                pass

            # Turn someone into a fortune teller
            if role in ["Fortune Teller"]:
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

    if int(db_get(user_id,'frozen')) == 1:
        return answer.log("<@{}> was frozen and couldn't get killed by the **{}**.".format(user_id,role))
    if int(db_get(user_id,'abducted')) == 1:
        return answer.log("<@{}> couldn't get attacked because they were **abducted**.".format(user_id))

    user_role = db_get(user_id,'role')

    if user_role in ['Sacred Wolf']:
        return answer.log('The **Sacred Wolf** <@{}> was protected from death.'.format(user_id))
    
    if db.has_amulet(user_id):
        return answer.log("<@{}> was protected from the **{}** by their amulet.".format(user_id,role))

    souls = db_get(user_id,'souls')
    if souls > 0:
        db_set(user_id,'souls',souls-1)
        return answer.log('<@{}> lost a soul, but survived an attack.')

    # Save the dude if they're demonized
    if int(db_get(user_id,'demonized')) == 1:
        if user_role not in ["Exorcist","Devil","Demon","Horseman","The Thing","Undead","Vampire","Zombie"]:

            db_set(user_id,'undead',1)
            answer.dm("Last night, you didn't feel to well and decided to go out, to take a walk. ",user_id)
            answer.dm_add("As soon as you stepped out the door, you felt like it was a bad idea - and it was!\n")
            answer.dm_add("The last thing you can remember is the sound of someone approaching you from behind, ")
            answer.dm_add("the sound of a skull cracking open, and then - **NOTHING**.\n\n")
            answer.dm_add("Is this the end?\n\n")
            answer.dm_add("It doesn't appear so. You wake up in a graveyard. A few cold and grim silhouettes ")
            answer.dm_add("stand in front of you. You are surrounded, but it feels more... welcoming. ")
            answer.dm_add("And then the truth arrives.\n")
            answer.dm_add("The **{}** you once were, is dead. Their soul could not rest, and that is you. ")
            answer.dm_add("The remainders of something that wasn't ready to die.\n")
            answer.dm_add("**You have become Undead. Murder everyone that isn't an undead or a vampire.")

            for channel_id in db.get_secret_channels('Undead'):
                answer.edit_cc(channel_id,user_id,1)
                answer.msg("Last night, <@{}>, a **{}** has died! Please welcome them in the realm of the Undead!",channel_id)

            if user_role not in pos.pretenders:
                db_set(user_id,'role','Undead')
                answer.dm_add("**")
            else:
                answer.dm_add(" Your former teammates do not know you are Undead, so make use of this advantage.**")
            
            return answer

    # If there's nothing to save this pool soul... well, just kill 'em already.
    return suicide(user_id,answer)

def suicide(user_id,answer):
    """Kill a user. If there's nothing left, and you are ABSOLUTELY SURE the player dies, execute this function."""
    db_set(user_id,'role','Dead')
    db_set(user_id,'fakerole','Dead')
    db_set(user_id,'horseman',0)
    
    # Change all channel settings
    for channel_id in db.channel_change_all(user_id,1,4):
        answer.edit_cc(channel_id,user_id,4)
    for channel_id in db.channel_change_all(user_id,2,4):
        answer.edit_cc(channel_id,user_id,4)
    for channel_id in db.channel_change_all(user_id,5,4):
        answer.edit_cc(channel_id,user_id,4)

    for channel_id in db.channel_change_all(user_id,3,7):
        answer.edit_cc(channel_id,user_id,7)
    for channel_id in db.channel_change_all(user_id,6,7):
        answer.edit_cc(channel_id,user_id,7)

    if int(db_get(user_id,'abducted')) == 0:
        db.insert_deadie(user_id)
    
    # Kill all standoffs, right here, on the spot.
    # Yes, this is gonna become a recursive function! But don't worry!
    # Look at the top of this function, I implemented an exit condition.
    # Hold on, I need to reconsider how I'm gonna do this.

    # Thinky Thonkie Thonk

next = '|            '
success = '|---> '
failure = '|\n'
skull = '💀 '

def attack(user_id,role,murderer,answer=Mailbox().log(''),recursive='\n'):
    """This functions attacks the given player with the given role.  
    The effects are immediate, but they can be used in all scenarios, as only\
    standoffs are executed during this attack."""
    
    user_role = db_get(user_id,'role')
    answer.log_add(recursive + failure)

    demonized = False
    if int(db_get(user_id,'demonized')) == 1:
        demonized = True
    
    undead = False
    if int(db_get(user_id,'undead')) == 1 or user_role == 'Undead':
        undead = True
        demonized = False

    # End function if player is dead (exit condition for recursion)
    if user_role in ['Dead','Spectator','Suspended',None,'Unknown']:
        return answer.log_add(recursive + success + '<@{}> was already dead!'.format(user_id))
    
    if role == 'Cupid':
        answer.log_add(recursive + success + skull + '<@{}> committed suicide.')
        answer = instant_death(user_id, answer, recursive+next)
        if int(db_get(user_id,'abducted')) != int(db_get(murderer,'abducted')):
            answer.dm("Abducted or not, you know your lover has deceased! ",user_id)
            answer.dm_add("You couldn't handle the pain, and that's why you decided to put an end to it.\n")
            answer.dm_add("Your story ends here.")
        elif int(db_get(user_id,'frozen')) == 1:
            answer.dm("Even though your heart has become cold from the ice surrounding you, ",user_id)
            answer.dm_add("but it got even colder when you saw the dead body of <@{}> being carried away.\n".format(murderer))
            answer.dm_add("It was at this moment where the ice got even colder...")
        else:
            answer.dm("You couldn't bear the sight of your lover, <@{}>, ".format(murderer),user_id)
            answer.dm_add("lying dead in your arms. This is why you have decided to end it all!\n")
            answer.dm_add("Let\'s just hope this isn\'t like Romeo and Juliet...")
        answer.dm_add("**Your lover <@{}> has died. In response, you have committed suicide.**")
        return answer

    if role == 'Fortune Teller':
        if not undead:
            answer.dm("Your idol, the fortune teller <@{}>, has deceased. ".format(murderer),db_get(user_id,'channel'))
            answer.dm_add("They were a great inspiration to you, and that's why ")
            answer.dm_add("you've decided to get in their footsteps!\n")
            answer.dm_add("**You have turned into a Fortune Teller. Find and ")
            answer.dm_add("eliminate all werewolves, solo players and other enemies!**")
            answer.log_add(recursive + success + '<@{}> became a fortune teller.')
        else:
            answer.dm("Your idol, the fortune teller <@{}>, has deceased. ".format(murderer),user_id)
            answer.dm_add("They were a great inspiration to you... ")
            answer.dm_add("back when you were alive, at least. Now, your undead heart is as cold as it has ever been, ")
            answer.dm_add("and nothing will happen to you.\n")
            answer.dm_add("**The rules have changed. You will remain Undead.**")
            answer.log_add(recursive + success + '<@{}> failed to become a fortune teller.')
            db_set(user_id,'role','Fortune Teller')
        return answer

    # End if user is frozen.
    if int(db_get(user_id,'frozen')) == 1:
        return answer.log_add(recursive + success + '<@{}> was frozen and thus protected.'.format(user_id))

    # Let all zombies kill all other zombies.
    if role == "Zombie":
        answer.log_add(recursive + success + skull + '<@{}> has decayed.'.format(user_id))
        answer = instant_death(user_id, answer, recursive+next)
        return answer

    # Kill abducted players (or The Thing himself)
    if role == "The Thing":
        answer.log_add(recursive + success + skull + '<@{}> was killed.'.format(user_id))
        # TODO: kill the player (BUT NOT THROUGH THE SUICIDE FUNCTION)
        return answer

    # End if user is immortal.
    if user_role == "Immortal":
        answer.log_add(recursive + success + '<@{}> is immortal.'.format(user_id))

    # End if user is abducted.
    if int(db_get(user_id,'abducted')) == 1:
        return answer.log_add(recursive + success + '<@{}> was abucted and thus protected.')

    # End if the user sleeps with another.
    if role == "Hooker" and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was hooked.')
        answer = instant_death(user_id, answer, recursive+next)
        return answer
    
    # End if player dies in someone else's place.
    if role == "Executioner":
        answer.log_add(recursive + success + skull + '<@{}> was executed.')
        answer = instant_death(user_id, answer, recursive+next)
        return answer
    
    # End if player dies in someone else's place.
    if role == "Huntress":
        answer.log_add(recursive + success + skull + '<@{}> was shot.')
        answer = instant_death(user_id, answer, recursive+next)
        return answer

    # Kill whoever stands in the barber's way!
    if role == "Barber":
        answer.log_add(recursive + success + skull + '<@{}> was cut to death.')
        answer = instant_death(user_id, answer, recursive+next)
        return answer.story(barber_kill_story(murderer,user_id))

    # Check if user has an amulet.
    if db.has_amulet(user_id):
        return answer.log_add(recursive + success + "<@{}> was protected by their amulet.")
    
    # Kill assassinations
    if role == 'Assassin' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was assassinated.'.format(user_id))
        answer = instant_death(user_id, answer, recursive+next)
        return answer
    if role == 'Cult Leader' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was killed by the cult.')
        answer = instant_death(user_id, answer, recursive+next)
        return answer
    if role == 'Priest' and not demonized:
        if user_role in pos.wolf_team:
            answer.log_add(recursive + success + skull + '<@{}> was holified.'.format(user_id))
            answer = instant_death(user_id, answer, recursive+next)
            return answer
    if role == 'Witch' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was poisoned.')
        answer = instant_death(user_id, answer, recursive+next)
        return answer
    
    # Kill wolf attacked
    if role in ['Werewolf','Lone Wolf','White Werewolf']:
        if user_role == 'Runner':
            answer.log_add(recursive + success + '<@{}> outran a wolf attack.')
            answer.dm('You. Are. EXHAUSTED.\n',user_id)
            answer.dm_add('Last night may have been the worst night of your life! ')
            answer.dm_add('You\'re still alive, however. And that\'s what counts. ')
            answer.dm_add('Let\'s hope that, whatever those creatures were, won\'t attack again tomorrow night!\n')
            answer.dm_add('**Last night, you have been attacked by a wolf. You have become a regular Innocent.**')
            db_set(user_id,'role','Innocent')
            return answer
        if user_role == 'Cursed Civilian':
            answer.dm("The curse that went around you, had been a little itchy lately... and it kept getting worse! ",user_id)
            answer.dm_add("It got worse and worse, and you couldn't help but notice how hair started growing everywhere!\n")
            answer.dm_add("Last night, you were waking up by the grunts of a what sounded like a wolf! ")
            answer.dm_add("You thought your days were over, but the wolf did not attack. Instead, ")
            answer.dm_add("the wolf watched as your nails grew longer, your ears became spiky and your smell ")
            answer.dm_add("slowly improved... and you looked just like one of the silhouettes in the shadow, ")
            answer.dm_add("waiting for you to join them in the beautiful night's sky...\n")
            answer.dm_add("**You have been visited by wolves last night, and your curse made you turn ")
            answer.dm_add("into a werewolf. Devour all villagers and win the game!**")

            db_set(user_id,'role','Werewolf')
            answer.log_add(recursive + success + '<@{}> has turned into a Werewolf!')

            for channel_id in db.get_secret_channels('Werewolf'):
                answer.edit_cc(channel_id,user_id,1)
                answer.msg("**ARRROOOO!\nWelcome, <@{}>!**".format(user_id),channel_id)
                answer.msg_add("Last night, the **cursed civilian** <@{}> was attacked by wolves, ")
                answer.msg_add("and has now become a **werewolf**! Please, welcome this new member ")
                answer.msg_add("of the wolf pack!")
            return answer
        
        answer.log_add(recursive + success + skull + '<@{}> was eaten by a werewolf.')
        answer = instant_death(user_id, answer, recursive+next)
        return answer

    # TODO
    return answer

def instant_death(user_id,answer=Mailbox().log(''),recursive=''):
    """Eliminate the given user."""

    # TODO
    return answer
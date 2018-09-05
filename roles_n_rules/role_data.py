night_users = [
    ["Cupid","Dog","Look-Alike"],
    ["Assassin","Aura Teller","Exorcist","Fortune Teller","Hooker","Innkeeper","Priest","Priestess","Raven","Curse Caster",
        "Infected Wolf","Lone Wolf","Warlock","Devil","Ice King","Pyromancer","The Thing","Vampire","Zombie"],
    [],
    ["Crowd Seeker","Grandma"]
    ]

day_users = [[],["Barber","Royal Knight"],[],["Tanner"]]

import management.position as pos
import management.db as db
import management.dynamic as dy
from config import universal_prefix as unip
from management.db import db_get, db_set
from main_classes import Mailbox
from management.dynamic import lifepotion_in_play
from story_time.barber_kills import barber_kill_story

next = '|            '
success = '|---> '
failure = '|'
skull = '💀 '

def attack(user_id,role,murderer,answer=Mailbox().log(''),recursive='\n'):
    """This functions attacks the given player with the given role.  
    The effects are immediate, but they can be used in all scenarios, as only\
    standoffs are executed during this attack."""

    if role == 'Inactive':
        answer.log_add(recursive + success + skull + "<@{}> was killed due to inactivity.".format(user_id))
        return instant_death(user_id, role, answer, recursive + next)

    # Prevent Pyromancer from causing way too long lines
    # No, I didn't add this during debugging.
    # Yes, that means I planned to design it this terribly.
    if role == 'Pyromancer' and int(db_get(user_id,'powdered')) != 1:
        return answer

    user_role = db_get(user_id,'role')
    answer.log_add(recursive + failure)

    try:
        demonized = False
        if int(db_get(user_id,'demonized')) == 1:
            demonized = True

        undead = False
        if int(db_get(user_id,'undead')) == 1 or user_role == 'Undead':
            undead = True
            demonized = False
    except Exception:
        demonized = False
        undead = False

    # End function if player is dead (exit condition for recursion)
    if user_role in ['Dead','Spectator','Suspended',None,'Unknown']:
        return answer.log_add(recursive + success + '<@{}> was already dead!'.format(user_id))

    if role == 'Cupid':
        answer.log_add(recursive + success + skull + '<@{}> committed suicide.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
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
        answer.dm_add("**Your lover, <@{}>, has died. In response, you have committed suicide.**".format(murderer))
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
    
    if role == 'Horseman' and user_role == 'Horseman':
        horse_number = db_get(user_id, 'horseman')
        apocalypse_ready = True
        for player in db.player_list():
            if int(db_get(player,'horseman')) != 0:
                apocalypse_ready = False
            if int(db_get(player,'horseman')) == horse_number:
                db_set(player, 'horseman', 0)
        answer.log_add(recursive + success + '<@{}> was united.'.format(user_id))

        if horse_number != 0:
            for channel_id in db.get_secret_channels('Horseman'):
                answer.msg('**Horseman #{} has been united!**'.format(horse_number),channel_id)
        
        if apocalypse_ready:
            for player in db.player_list():
                if db_get(player,'role') == 'Horseman':
                    answer.log_add(recursive + next + failure)
                    answer.log_add(recursive + next + success + '<@{}> has joined the **Apocalypse**!')
                    db_set(player,'horseman',5)
                    
                    answer.secret_dm('All Horsemen are united! This means that the **APOCALYPSE** can be unleashed!','Horseman')
            answer.story('Oh no! The Apocalypse has been unleashed!')
        return answer


    # End if user is frozen.
    if int(db_get(user_id,'frozen')) == 1:
        return answer.log_add(recursive + success + '<@{}> was frozen and thus protected.'.format(user_id))

    if role == "Devil":
        if user_role == 'Devil':
            answer.log_add(recursive + success + '<@{}> did not die to their own wage.')
            return answer
        answer.log_add(recursive + success + skull + '<@{}> was killed by the wager.')
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer

    # Let all zombies kill all other zombies.
    if role == "Zombie":
        answer.log_add(recursive + success + skull + '<@{}> has decayed.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer

    # Kill abducted players (or The Thing himself)
    if role == "The Thing":
        answer.log_add(recursive + success + skull + '<@{}> was killed.'.format(user_id))
        # TODO: kill the player (BUT NOT THROUGH THE SUICIDE FUNCTION)
        return answer

    # End if user is immortal.
    if user_role == "Immortal":
        answer.log_add(recursive + success + '<@{}> is immortal.'.format(user_id))
        return answer

    # End if user is abducted.
    if int(db_get(user_id,'abducted')) == 1:
        return answer.log_add(recursive + success + '<@{}> was abucted and thus protected.'.format(user_id))

    # Kill lynch!
    if role == "Innocent":
        replacements = [standoff for standoff in db.get_standoff(user_id) if standoff[2] == 'Executioner']

        if replacements == []:
            answer.log_add(recursive + success + skull + '<@{}> was killed by an angry mob.'.format(user_id))
            answer = instant_death(user_id, role, answer, recursive+next)
            
        else:
            answer.log_add(recursive + success + '<@{}> escaped death as the Executioner.')
            
            if user_role == 'Executioner':
                db_set(user_id,'role','Innocent')

            for standoff in replacements:
                db.delete_standoff(standoff[0])
                answer = instant_death(standoff[1], standoff[2], answer, recursive+next)

        return answer

    # Kill whoever stands in the barber's way!
    if role == "Barber":
        answer.log_add(recursive + success + skull + '<@{}> was cut to death.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer.story(barber_kill_story(murderer,user_id))
    
    # Save users if they have souls to spare.
    souls = int(db_get(user_id,'souls'))
    if souls > 0:
        db_set(user_id,'souls',souls-1)
        answer.log_add(recursive + success + '<@{}> lost a soul.'.format(user_id))
        return answer

    # End if the user sleeps with another.
    if role == "Hooker" and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was hooked.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer
    
    # End if player dies in someone else's place.
    if role == "Executioner":
        answer.log_add(recursive + success + skull + '<@{}> was executed.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer
    
    # End if player dies in someone else's place.
    if role == "Huntress" and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was shot.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer

    # Check if user has an amulet.
    if db.has_amulet(user_id) and role not in ['Hooker']:
        return answer.log_add(recursive + success + "<@{}> was protected by their amulet.".format(user_id))

    # Protect apocalypse horsemen
    if int(db_get(user_id,'horseman')) == 5:
        return answer.log_add('<@{}> was protected by the Apocalypse.'.format(user_id))
    
    # Kill assassinations
    if role == 'Assassin' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was assassinated.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer
    if role == 'Cult Leader' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was killed by the cult.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer
    if role == 'Priest' and not demonized:
        if user_role in pos.wolf_team:
            answer.log_add(recursive + success + skull + '<@{}> was holified.'.format(user_id))
            answer = instant_death(user_id, role, answer, recursive+next)
            return answer
    if role == 'Witch' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was poisoned.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer
    
    # Kill wolf attacked
    if role in ['Werewolf','Lone Wolf','White Werewolf']:
        if user_role == 'Runner':
            answer.log_add(recursive + success + '<@{}> outran a wolf attack.'.format(user_id))
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
            answer.log_add(recursive + success + '<@{}> has turned into a Werewolf!'.format(user_id))

            for channel_id in db.get_secret_channels('Werewolf'):
                answer.edit_cc(channel_id,user_id,1)
                answer.msg("**ARRROOOO!\nWelcome, <@{}>!**".format(user_id),channel_id)
                answer.msg_add("Last night, the **cursed civilian** <@{}> was attacked by wolves, ".format(user_id))
                answer.msg_add("and has now become a **werewolf**! Please, welcome this new member ")
                answer.msg_add("of the wolf pack!")
            return answer
        if not demonized:
            answer.log_add(recursive + success + skull + '<@{}> was eaten by a werewolf.'.format(user_id))
            answer = instant_death(user_id, role, answer, recursive+next)
            return answer
    
    # Kill solo attacked
    if role == 'Demon' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was sent to hell.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer
    if role == 'Horseman' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> was apocalypsed.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer
    if role == 'Pyromancer' and not demonized:
        answer.log_add(recursive + success + skull + '<@{}> went up in flames.'.format(user_id))
        answer = instant_death(user_id, role, answer, recursive+next)
        return answer

    # Assume they were supposed to be killed, but that they are demonized. Let's turn them undead!
    answer.log_add(recursive + success + skull + '<@{}> has become undead.')

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

def instant_death(user_id, role, answer=Mailbox().log(''),recursive=''):
    """Eliminate the given user."""

    # If the user was reporter or mayor, get rid of that.
    if dy.get_mayor() == user_id:
        dy.kill_mayor()
        answer.remove_proms(user_id)
    if dy.get_reporter() == user_id:
        dy.kill_reporter()
        answer.remove_proms(user_id)

    for channel_id in db.get_secret_channels("Graveyard"):
        answer.edit_cc(channel_id,user_id,1)

    # Change all channel settings
    for channel_id in db.channel_change_all(user_id,1,4):
        answer.edit_cc(channel_id,user_id,4)
    for channel_id in db.channel_change_all(user_id,2,4):
        answer.edit_cc(channel_id,user_id,4)
    for channel_id in db.channel_change_all(user_id,5,4):
        answer.edit_cc(channel_id,user_id,4)

    # Change abducted settings
    for channel_id in db.channel_change_all(user_id,3,7):
        answer.edit_cc(channel_id,user_id,7)
    for channel_id in db.channel_change_all(user_id,6,7):
        answer.edit_cc(channel_id,user_id,7)

    # Kill that user already! 
    db_set(user_id,'role','Dead')
    db_set(user_id,'fakerole','Dead')

    answer.spam(unip + 'kill <@{}>'.format(user_id))

    if int(db_get(user_id,'abducted')) != 1:
        db.insert_deadie(user_id)
    
    # Kill all standoffs
    for taker in db.get_standoff(user_id):
        answer = attack(taker[1],taker[2],taker[3],answer,recursive)

    return answer
import roles_n_rules.commands as ctory
import management.db as db
import random
from management.position import wolf_pack
from management.db import db_get, db_set
from main_classes import Mailbox
from config import game_master
from config import ww_prefix as prefix

def see(user_id,victim_id):
    """This function allows the user to see a given player of their choice.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who casts the spell
    victim_id -> the player who is being searched"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to see this player!",True)
    db_set(user_id,'uses',uses - 1)

    victim_emoji = db_get(victim_id,"emoji")
    victim_fakerole = db_get(victim_id,"fakerole")
    victim_role = db_get(victim_id,"role")
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(user_id,'abducted'))

    user_channel = int(db_get(user_id,"channel"))
    user_undead = int(db_get(user_id,'undead'))
    user_role = db_get(user_id,"role")

    if user_undead == 1:
        return Mailbox().dm("You are undead! This means that you can no longer inspect players. I\'m sorry!",user_id)
    if victim_frozen == 1:
        return Mailbox().msg("You have tried to inspect <@{}>, but it turns out you couldn\'t reach them through the ice! Luckily, you had the opportunity to try again.",user_channel,True)
    if victim_abducted == 1:
        return Mailbox().msg("You tried to see <@{}>... but you couldn\'t find them! Almost as if they had disappeared in thin air!\nWhat happened?",user_channel,True)

    # Follow this procedure if the user has been enchanted.
    if int(db_get(user_id,"echanted")) == 1 and random.random() < 0.6:
        answer = Mailbox().msg("{} - <@{}> has the role of the `Flute Player`!".format(victim_emoji,victim_id),user_channel)
        answer.log("<@{0}> has attempted to see the role of <@{1}>. However, their enchantment effect worked, showing <@{1}> as the **Flute Player!**".format(user_id,victim_id))

        # Easter egg
        if victim_role == "Flute Player":
            answer.log("I mean, <@{}> *is* a **Flute Player**, so it wouldn't really matter. But hey! They don't need to know. 😉")

        return answer

    answer = Mailbox().msg("{} - <@{}> has the role of the `{}`!".format(victim_emoji,victim_id,victim_fakerole),user_channel)

    if victim_fakerole != victim_role:
        answer.log("<@{}>, the town's **{}**, has attempted to see <@{}>, the **{}**. ".format(user_id,user_role,victim_id,victim_role))
        return answer.log_add("However, they were disguised and appeared to be the **{}**!".format(victim_fakerole))

    return answer.log("<@{}>, a **{}**, has seen the role of <@{}>, who had the role of the **{}**!".format(user_id,user_role,victim_id,victim_role))

def disguise(user_id,victim_id,role):
    """This fuction is taking the tanner's action of disguising people.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who casts the spell
    victim_id -> the player upon whom the spell is cast
    role -> the role the player should be disguised as"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to disguise anyone!",True)
    db_set(user_id,'uses',uses - 1)

    user_channel = int(db_get(user_id,'channel'))
    user_role = db_get(user_id,'role')
    user_undead = int(db_get(user_id,'undead'))

    victim_role = db_get(victim_id,'role')
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    if user_undead == 1:
        return Mailbox().dm("I am sorry! You are undead, meaning you can no longer disguise people!",user_id)
    if victim_frozen == 1:
        return Mailbox().msg("I am sorry, but <@{}> is too cold for that! You\'ll need a lot more than warm suit to get \'em warmed up.".format(victim_id),user_channel)
    if victim_abducted == 1:
        return Mailbox().msg("After having finished your great disguise, it seems like you couldn\'t find your target! Where have they gone off to?",user_channel)

    db_set(victim_id,'fakerole',role)
    answer = Mailbox().msg("You have successfully disguised <@{}> as the **{}**!".format(victim_id,role),user_channel)

    if uses - 1 > 0:
        answer.msg("You can disguise **{}** more players!".format(uses-1),user_channel,True)
    else:
        answer.msg("That\'s it for today! You can\'t disguise any more players.",user_channel,True)

    return answer.log("**{}** <@{}> has disguised <@{}>, the **{}**, as the **{}**!".format(user_role,user_id,victim_id,victim_role,role))

def nightly_kill(user_id,victim_id):
    """This function adds a kill to the kill queue based on the user's role.
    This function is applicable for roles like the assassin, the lone wolf, the priest, the thing and the white werewolf.
    NOTICE: This function is meant for people who kill solo! Teams should receive a poll.
    Evaluating whether the kill should actually be applied isn't needed, as this is evaluated at the start of the day.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who will initiate the attack
    victim_id -> the player who shall be \"attacked\""""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have this ability available!",True)
    db_set(user_id,'uses',uses - 1)

    user_role = db_get(user_id,'role')
    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))

    if user_undead == 1:
        return Mailbox().dm("I am sorry! An undead cannot use this power!",user_id)

    # Add kill to the kill queue
    db.add_kill(victim_id,user_role,user_id)

    answer = Mailbox().msg(ctory.kill_acceptance(victim_id),user_channel)
    return answer.log("The **{}** <@{}> has chosen to pay a visit to <@{}> tonight.".format(user_role,user_id,victim_id))

def powder(user_id,victim_id):
    """This function powders a player if they are alive and not a pyromancer.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who powders the victim
    victim_id -> the player who is powdered"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently cannot powder anyone!",True)
    db_set(user_id,'uses',uses - 1)

    user_role = db_get(user_id,'role')
    user_channel = db_get(user_id,'channel')
    user_undead = int(db_get(user_id,'undead'))

    victim_role = db_get(victim_id,'role')
    victim_powdered = int(db_get(victim_id,'powdered'))

    if victim_role == 'Pyromancer':
        return Mailbox().msg("I am sorry, <@{}>, but you cannot powder a pyromancer!".format(user_id),user_channel,True)
    if victim_powdered == 1:
        return Mailbox().msg("I am terribly sorry, but <@{}> has already been powdered! Please choose another victim.".format(victim_id),user_channel,True)

    # Powder the player
    answer = Mailbox().msg("You have successfully powdered <@{}>!".format(victim_id),user_channel)
    if user_undead == 1:
        answer.log("<@{}>, an undead, has pretended to powder <@{}>.".format(user_id,victim_id))
        return answer.dm("Hey, you are undead, so your powers no longer work... but here\'s a little help to keep up your cover!",user_id)

    db_set(victim_id,'powdered',1)
    return answer.log("The **{}** <@{}> has powdered the **{}** <@{}>!".format(user_role,user_id,victim_role,victim_id))

def ignite(user_id):
    """This function ignites all powdered players that aren't pyromancer.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who ignites all powdered players"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently cannot ignite anyone!",True)
    db_set(user_id,'uses',uses - 1)

    user_role = db_get(user_id,'role')
    user_channel = db_get(user_id,'channel')
    user_undead = int(db_get(user_id,'undead'))

    if user_undead == 1:
        answer = Mailbox().log("<@{}>, an undead **{}**, has pretended to ignite all powdered players.".format(user_id,user_role))
        answer.dm("Hey, you are undead, so your power won\'t work. But at least this won\'t blow your cover!",user_id)
        return answer.msg("Okay! All powdered players will die tomorrow.",user_channel)

    # Ignite all living players.
    for user in db.player_list():
        if db.isParticipant(user):
            db.add_kill(int(user),'Pyromancer',user_id)

    answer = Mailbox().log("The **{}** <@{}> has ignited all powdered players!".format(user_role,user_id))
    return answer.msg("Okay! All powdered players will die tomorrow.",user_channel)

def freeze(user_id,victim_id,role = ''):
    """This function allows the ice king to guess a player's role. As the roles are evaluated once all guesses
    have been submitted, it is not yet determined whether the guess was correct or incorrect.
    The function will remove the given user from the list of guesses if no role has been given.

    user_id -> the ice king's id
    victim_id -> the id of the user that is being guessed
    role -> the role that is being guessed"""

    answer = Mailbox()

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return answer.respond("I am sorry! You currently cannot guess anyone\'s role!",True)

    user_channel = db_get(user_id,'channel')
    user_undead = int(db_get(user_id,'undead'))

    if role != '':
        change = db.add_freezer(user_id,victim_id,role)
        if change == None:
            answer.msg("<@{}> has been added to your freeze list as a **{}**!".format(victim_id,role),user_channel,True)
        else:
            answer.msg("You originally guessed <@{}> to be a **{}**, but I now changed it to the **{}**!".format(victim_id,change,role),user_channel,True)
    else:
        if db.delete_freezer(user_id,victim_id) == True:
            answer.msg("You have removed <@{}> from your freeze list.".format(victim_id),user_channel,True)
        else:
            return answer.msg("**Invalid syntax:**\n\n`" + prefix + "freeze <user> <role>`\n\n**Example:** `" + prefix + "freeze @Randium#6521 Pyromancer`",user_channel,True)

    if user_undead == 1:
        answer.dm("Hey, you are undead, so you can\'t really freeze anyone. But at least this won\'t blow your cover!",user_id,True)

    return answer

def aura(user_id,victim_id):
    """This function allows the aura teller to inspect if a given user is among the wolf pack or not.
    The function assumes the player is an aura teller and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who casts the spell
    victim_id -> the player who is being searched"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to see this player!",True)
    db_set(user_id,'uses',uses - 1)

    victim_emoji = db_get(victim_id,"emoji")
    victim_role = db_get(victim_id,"role")
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    user_channel = int(db_get(user_id,"channel"))
    user_undead = int(db_get(user_id,'undead'))
    user_role = db_get(user_id,"role")

    if user_undead == 1:
        return Mailbox().dm("You are undead! This means that you can no longer inspect players. I\'m sorry!",user_id)
    if victim_frozen == 1:
        return Mailbox().msg("You have tried to inspect <@{}>, but it turns out you couldn\'t see their aura all the way through the ice! Luckily, you had the opportunity to try again.",user_channel,True)
    if victim_abducted == 1:
        return Mailbox().msg("You tried to inspect <@{}>... but their aura seemed empty! Almost as if they weren't there!\nYou decided to inspect someone else.",user_channel,True)

    if victim_role in wolf_pack:
        answer = Mailbox().msg("🐺 - <@{}> has a **RED AURA** - they are taking part in the wolf pack!".format(victim_id),user_channel)
        return answer.log("The **Aura Teller** <@{}> has inspected the **{}** <@{}>, and found out they were part of the wolf pack!".format(user_id,victim_role,victim_id))

    answer = Mailbox().msg("🐶 - <@{}> has a **GREEN AURA** - they are not taking part in the wolf pack.".format(victim_id),user_channel)
    return answer.log("The **Aura Teller** <@{}> has inspected <@{}>, who, being the **{}**, wasn't part of the wolf pack.".format(user_id,victim_id,victim_role))

def cupid_kiss(user_id,victim_id):
    """This function makes the cupid fall in love with a partner.
    The function assumes the player is a cupid and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the cupid who casts the spell
    victim_id -> the player who's falling in love with the cupid"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently cannot choose someone to fall in love with!",True)
    db_set(user_id,'uses',uses - 1)

    user_channel = int(db_get(user_id,'channel'))

    victim_role = db_get(victim_id,'role')
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))
    victim_undead = int(db_get(victim_id,'undead'))

    if victim_frozen == 1:
        return Mailbox().msg("Your love arrows just do not seem to be able to reach your chosen lover! They are frozen! Please try someone else.",user_channel,True)
    if victim_abducted == 1:
        return Mailbox().msg("You wanted to throw an arrow at your target... but you cannot find them! It's almost as if they had disappeared from this town!",user_channel,True)

    answer = Mailbox().edit_cc(user_channel,victim_id,1).dm("Welcome, <@{}>!".format(victim_id),user_channel)
    answer.log("The **Cupid** <@{}> has chosen to fall in love with <@{}>.".format(victim_id))
    answer.dm("Hello there, <@{}>! The **Cupid** <@{}> has chosen to fall in love with you!\n".format(user_id))
    answer.dm_add("For the rest of the game, you two will remain partners. Be open and honest, as you cannot win if the other dies!\n")
    answer.dm_add("Good luck!").msg("<@{}> and <@{}> have fallen in love with each other! ".format(user_id,victim_id))

    if victim_undead == 1:
        answer.msg_add("<@{}>, while pretending to be a **{}**, is secretly an **Undead**!".format(victim_id,victim_role))
    else:
        answer.msg_add("<@{}>, the town's favourite **{}**, has decided to trust <@{}>.".format(victim_id,victim_role,user_id))

    return answer.msg_add("\nTogether, they will survive this town!")

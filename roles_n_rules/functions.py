import story_time.roleswap_msg as rolestory
import story_time.commands as ctory
import management.db as db
import random
from management.position import wolf_pack
from management.db import db_get, db_set
from main_classes import Mailbox
from config import game_master
from config import ww_prefix as prefix

# --------------------------------------------------
#
#               WORKING ROLES
#
# --------------------------------------------------
# The following roles have been tested thoroughly and are known to work.

# Dog
def dog_follow(user_id,role):
    """This function allows the dog to choose a role to become.
    The function assumes the player is a cupid and has provided a role, so make sure to have filtered this out already.
    The role does not need to be Innocent, Cursed Civilian or Werewolf yet.
    The function returns a Mailbox.

    user_id -> the dog who chooses a role
    role -> the role they'd like to be"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently cannot choose a role to become!",True)

    user_channel = int(db_get(user_id,'channel'))

    if role not in ['Innocent', 'Cursed Civilian', 'Werewolf']:
        return Mailbox().msg("I'm sorry, <{}>. Being a dog lets you choose a role, but it doesn't mean you can become ANYTHING.".format(user_id),user_channel,True)

    db_set(user_id,'uses',uses - 1)

    answer = Mailbox().msg("You have chosen to become the **{}**!".format(role),user_channel)
    answer.log("The **Dog** <@{}> has chosen to become a".format(user_id))

    if role == 'Innocent':
        answer.log_add('n **Innocent**!').dm("You have chosen to become an **Innocent**. Protect the town, kill all those wolves!",user_id)
    if role == 'Cursed Civilian':
        answer.log_add(' **Cursed Civilian**!').dm("You have chosen to become a **Cursed Civilian**! You will be part of the town... for now.",user_id)
    if role == 'Werewolf':
        answer.log_add(' **Werewolf**!').dm("You have chosen to become a **Werewolf**! You will now join the wolf pack!",user_id)
        for channel_id in db.get_secret_channels("Werewolf"):
            answer.edit_cc(channel_id,user_id,1)
            if int(db_get(user_id,'frozen')) == 1:
                answer.edit_cc(channel_id,user_id,2)
            answer.msg("**ARRROOOO!\nWelcome, <@{0}>, to the wolf pack!** <@{0}>, a **Dog**, has chosen to turn themselves into a Werewolf! Give them a warm welcome.".format(user_id),channel_id)

    db_set(user_id,'role',role)
    return answer


# --------------------------------------------------
#
#                  BETA ROLES
#
# --------------------------------------------------
# The following roles are still under development, or require some more testing.

# Fortune Teller
def see(user_id,victim_id):
    """This function allows the user to see a given player of their choice.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who casts the spell
    victim_id -> the player who is being searched"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to see this player!",True)

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
    if victim_abducted == 1:
        return Mailbox().msg("You tried to see <@{}>... but you couldn\'t find them! Almost as if they had disappeared in thin air!\nWhat happened?",user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("You have tried to inspect <@{}>, but it turns out you couldn\'t reach them through the ice! Luckily, you had the opportunity to try again.",user_channel,True)

    db_set(user_id,'uses',uses - 1)

    # Follow this procedure if the user has been enchanted.
    # It ensures there is a 40% chance they get their guess wrong.
    if int(db_get(user_id,"enchanted")) == 1 and random.random() < 0.6:
        answer = Mailbox().msg("*NOTE: You are enchanted, your result has a 40% chance of showing as the Flute player*\n{} - <@{}> has the role of the `Flute Player`!".format(victim_emoji,victim_id),user_channel)
        answer.log("<@{0}> has attempted to see the role of <@{1}>. However, being enchanted made <@{1}> show as the **Flute Player!**".format(user_id,victim_id))

        # Easter egg
        if victim_role == "Flute Player":
            answer.log("<@{}> has seen the role of <@{}> (**Flute Player**) due to their enchantment effects. But hey! They don't need to know they actually *are* a **Flute Player**!. 😉".format(user_id, victim_id))

        return answer

    # TODO: Add undead thing.

    elif int(db_get(user_id,"enchanted")) == 1:
        answer = Mailbox().msg("*NOTE: You are enchanted, your result has a 40% chance of showing as the Flute player*\n{} - <@{}> has the role of the `{}`!".format(victim_emoji,victim_id,victim_fakerole),user_channel)
    else:
        answer = Mailbox().msg("{} - <@{}> has the role of the `{}`!".format(victim_emoji,victim_id,victim_fakerole),user_channel)

    if victim_fakerole != victim_role:
        answer.log("<@{}>, the town's **{}**, has attempted to see <@{}>, the **{}**. ".format(user_id,user_role,victim_id,victim_role))
        return answer.log_add("However, they were disguised and appeared to be the **{}**!".format(victim_fakerole))

    return answer.log("<@{}>, a **{}**, has seen the role of <@{}>, who had the role of the **{}**!".format(user_id,user_role,victim_id,victim_role))

# Tanner
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

    user_channel = int(db_get(user_id,'channel'))
    user_role = db_get(user_id,'role')
    user_undead = int(db_get(user_id,'undead'))

    victim_role = db_get(victim_id,'role')
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    if user_undead == 1:
        return Mailbox().dm("I am sorry! You are undead, meaning you can no longer disguise people!",user_id,True)
    if victim_abducted == 1:
        return Mailbox().msg("After having finished your great disguise, it seems like you couldn\'t find your target! Where have they gone off to?",user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("I am sorry, but <@{}> is too cold for that! You\'ll need a lot more than warm suit to get \'em warmed up.".format(victim_id),user_channel,True)

    db_set(user_id,'uses',uses - 1)

    db_set(victim_id,'fakerole',role)
    answer = Mailbox().msg("You have successfully disguised <@{}> as the **{}**!".format(victim_id,role),user_channel)

    if uses - 1 > 0:
        answer.msg("You can disguise **{}** more players!".format(uses-1),user_channel,True)
    else:
        answer.msg("That\'s it for today! You can\'t disguise any more players.",user_channel,True)

    answer.log("**{}** <@{}> has disguised <@{}>, the **{}**, as the **{}**!".format(user_role,user_id,victim_id,victim_role,role))
    if victim_role == role:
        answer.log_add("\n...does that sound stupid? *Of course!* But how are they supposed to know?")
    return answer

# Priest, White Werewolf
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

    if user_id == victim_id:
        return Mailbox().respond("I am sorry, but you cannot attempt suicide!\nNot because it's not an option, no, just because we want to see you SUFFER!",True)

    # TODO: Prevent targeting of abducted/frozen players.
    if int(db_get(user_id,'undead')) == 1 or db_get(user_id,'role') == 'Undead':
        return Mailbox().respond("I am sorry! Now that you are Undead, you can no longer use this power.",True)
    if int(db_get(victim_id,'abducted')) == 1:
        return Mailbox().respond("You attempted to attack <@{}>... but they don't seem to be around in town! That is strange.".format(victim_id),True)
    if int(db_get(user_id,'frozen')) == 1:
        return Mailbox().respond("You wanted to pay a visit to <@{}>... but it seems they were frozen! Try again, please.".format(victim_id),True)

    user_role = db_get(user_id,'role')
    user_channel = int(db_get(user_id,'channel'))

    db_set(user_id,'uses',uses - 1)
    db.add_kill(victim_id,user_role,user_id)

    answer = Mailbox().msg(ctory.kill_acceptance(victim_id),user_channel)
    return answer.log("The **{}** <@{}> has chosen to pay <@{}> a visit tonight.".format(user_role,user_id,victim_id))

# Pyromancer
def powder(user_id,victim_id):
    """This function powders a player if they are alive and not a pyromancer.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who powders the victim
    victim_id -> the player who is powdered"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently cannot powder anyone!",True)

    user_role = db_get(user_id,'role')
    user_channel = db_get(user_id,'channel')
    user_undead = int(db_get(user_id,'undead'))

    victim_role = db_get(victim_id,'role')
    victim_powdered = int(db_get(victim_id,'powdered'))
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    if victim_id == user_id:
        return Mailbox().respond("I'm sorry, bud, you can't powder yourself.")
    if victim_abducted == 1:
        return Mailbox().msg("You have attempted to powder <@{}>... but you cannot find them! Have they left the town?".format(victim_id),user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("You tried to powder <@{}>... but it's not so easy to powder an ice cube! Let's try someone else.".format(victim_id),user_channel,True)
    if victim_role == 'Pyromancer':
        return Mailbox().msg("I am sorry, <@{}>, but you cannot powder a pyromancer!".format(user_id),user_channel,True)
    if victim_powdered == 1:
        return Mailbox().msg("I am terribly sorry, but <@{}> has already been powdered! Please choose another victim.".format(victim_id),user_channel,True)

    db_set(user_id,'uses',uses - 1)

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
    for user in db.player_list(True,True):
        if db.isParticipant(user) and user_role != 'Pyromancer':
            db.add_kill(int(user),'Pyromancer',user_id)

    answer = Mailbox().log("The **{}** <@{}> has ignited all powdered players!".format(user_role,user_id))
    return answer.msg("Okay! All powdered players will die tomorrow.",user_channel)

# Aura Teller
def aura(user_id,victim_id):
    """This function allows the aura teller to inspect if a given user is among the wolf pack or not.
    The function assumes the player is an aura teller and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who casts the spell
    victim_id -> the player who is being searched"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to see this player!",True)

    victim_role = db_get(victim_id,"role")
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    user_channel = int(db_get(user_id,"channel"))
    user_undead = int(db_get(user_id,'undead'))

    if user_undead == 1:
        return Mailbox().dm("You are undead! This means that you can no longer inspect players. I\'m sorry!",user_id)
    if victim_abducted == 1:
        return Mailbox().msg("You tried to inspect <@{}>... but their aura seemed empty! Almost as if they weren't there!\nYou decided to inspect someone else.",user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("You have tried to inspect <@{}>, but it turns out you couldn\'t see their aura all the way through the ice! Luckily, you had the opportunity to try again.",user_channel,True)

    db_set(user_id,'uses',uses - 1)

    if victim_role in wolf_pack:
        answer = Mailbox().msg("🐺 - <@{}> has a **RED AURA** - they are taking part in the wolf pack!".format(victim_id),user_channel)
        return answer.log("The **Aura Teller** <@{}> has inspected the **{}** <@{}>, and found out they were part of the wolf pack!".format(user_id,victim_role,victim_id))

    answer = Mailbox().msg("🐶 - <@{}> has a **GREEN AURA** - they are not taking part in the wolf pack.".format(victim_id),user_channel)
    return answer.log("The **Aura Teller** <@{}> has inspected <@{}>, who, being the **{}**, wasn't part of the wolf pack.".format(user_id,victim_id,victim_role))

# Cupid
def cupid_kiss(user_id,victim_id,voluntarily = True):
    """This function makes the cupid fall in love with a partner.
    The function assumes the player is a cupid and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the cupid who casts the spell
    victim_id -> the player who's falling in love with the cupid"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently cannot choose someone to fall in love with!",True)

    user_channel = int(db_get(user_id,'channel'))

    victim_role = db_get(victim_id,'role')
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))
    victim_undead = int(db_get(victim_id,'undead'))

    # If involuntary, make the cupid choose again.
    if voluntarily == False and (victim_id == user_id or victim_abducted == 1 or victim_frozen == 1):
        return False 

    if victim_id == user_id:
        return Mailbox().respond("So you wanna fall in love with yourself, huh? Too bad, your partner really has to be someone ELSE.")
    if victim_abducted == 1:
        return Mailbox().msg("You wanted to throw an arrow at your target... but you cannot find them! It's almost as if they had disappeared from this town!",user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("Your love arrows just do not seem to be able to reach your chosen lover! They are frozen! Please try someone else.",user_channel,True)

    db_set(user_id,'uses',uses - 1)

    answer = Mailbox().edit_cc(user_channel,victim_id,1).msg("Welcome, <@{}>!".format(victim_id),user_channel)
    answer.log("The **Cupid** <@{}> has chosen to fall in love with <@{}>.".format(user_id,victim_id))
    answer.dm("Hello there, <@{}>! The **Cupid** <@{}> has chosen to fall in love with you!\n".format(victim_id,user_id),victim_id)
    answer.dm_add("For the rest of the game, you two will remain partners. Be open and honest, as you cannot win if the other dies!\n")
    answer.dm_add("Good luck!")

    if victim_undead == 1:
        answer.msg_add("<@{}>, while pretending to be a **{}**, is secretly an **Undead**!".format(victim_id,victim_role))
    else:
        answer.msg_add("<@{}>, the town's favourite **{}**, has decided to trust <@{}>.".format(victim_id,victim_role,user_id))

    return answer.msg_add("\nTogether, they will survive this town!")


# Executioner
def executioner(user_id,victim_id):
    """This function allows the Executioner / huntress to choose a victim that will die in their place, may they get lynched during the day.
    The function assumes the player is a huntress and has provided a living participant, so make sure to have filtered this out already.
    The function returns a Mailbox.

    Keyword arguments:
    user_id -> the huntress/executioner's id
    victim_id -> the target's id"""

    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))
    role = db_get(user_id,'role')
    answer = Mailbox()

    if user_id == victim_id:
        return Mailbox().respond("I'm sorry, <@{}>. You cannot choose to kill yourself instead of yourself.".format(user_id))
    if user_undead == 1:
        return Mailbox().msg("I am sorry! Once you're undead, your target is set!",user_channel)

    user_found = False
    for action in db.get_standoff(user_id):
        if (action[2] == 'Huntress' or action[2] == 'Executioner') and role == action[2]:
            db.delete_standoff(action[0])
            if int(action[1]) != victim_id:
                user_found = True
                answer.msg("You no longer have <@{}> as your target.".format(int(action[1])),user_channel)

    db.add_standoff(victim_id,role,user_id)
    answer.msg("You have successfully chosen <@{}> as your ",user_channel)
    if user_found:
        answer.msg_add("new ")
    answer.msg_add("target!")

    return answer

# Grandma
def silence(user_id,victim_id):
    """This fuction is taking grandma's action of silencing people.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the grandma who silences the victim
    victim_id -> the player who shall be silenced"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to silence anyone!",True)

    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))

    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    if user_undead == 1:
        return Mailbox().dm("I am sorry! You are undead, meaning you can no longer silence people!",user_id)
    if victim_abducted == 1:
        return Mailbox().msg("It seems like <@{}> has disappeared! Oh well, at least then they won't make any noises either.",user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("Don't worry. <@{}>'s so cold, that they probably won't make any noise tomorrow.".format(victim_id),user_channel,True)

    db_set(user_id,'uses',uses - 1)

    db_set(victim_id,'votes',0)
    answer = Mailbox().msg("You have successfully silenced <@{}>!".format(victim_id),user_channel)

    if uses - 1 > 0:
        answer.msg("You can silence **{}** more players tonight!".format(uses-1),user_channel,True)
    else:
        answer.msg("That\'s it for tonight! You can\'t silence any more players.",user_channel,True)

    return answer.log("**Grandma** <@{}> has silenced <@{}>.".format(user_id,victim_id))

# Innkeeper
def unfreeze(user_id,victim_id):
    """This function allows the innkeeper to unfreeze frozen victims.
    The function assumes both players are participants, of which the casting user is an innkeeper. Make sure to have filtered this out already.
    The other user does not need to be frozen.
    The function returns a Mailbox.

    Keyword arguments:
    user_id -> the innkeeper who unfrozes a player
    victim_id -> the frozen player who is about to be unfrozen"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to unfreeze anyone!",True)

    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))

    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    if user_undead == 1:
        return Mailbox().msg("I'm sorry! You are undead, meaning that you can no longer unfreeze people!",user_channel,True)
    if victim_abducted == 1:
        return Mailbox().msg("You wanted to warm up <@{}>... but you weren't able to find them! That is strange...",user_channel,True)
    if victim_frozen == 0:
        return Mailbox().msg("This player isn't frozen! Please choose another target.",user_channel,True)

    db_set(user_id,'uses',uses - 1)
    db_set(victim_id,'frozen',0)

    answer = Mailbox().msg("You have successfully unfrozen <@{}>!".format(victim_id),user_channel)
    answer.unfreeze(victim_id)

    answer.dm("Great news, <@{}>! You have been unfrozen by an **Innkeeper**! You can now take part with the town again!".format(victim_id),victim_id)
    return answer.log("The **Innkeeper** <@{}> has unfrozen <@{}>.".format(user_id,victim_id))

# Priestess
def purify(user_id,victim_id):
    """This function allows the priestess to purify targets.
    The function assumes both players are participants, and that the casting user is a priestess. Make sure to have filtered this out beforehand.
    The function returns a Mailbox."""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to purify anyone!",True)

    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))

    victim_role = db_get(victim_id,'role')
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    if user_undead == 1:
        return Mailbox().msg("I am sorry! You cannot purify anyone while you're **Undead**!",user_channel,True)
    if victim_abducted == 1:
        return Mailbox().msg("You have attempted to purify <@{}>... but your powers cannot locate them! Strange...".format(victim_id),user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("You wanted to purify <@{}>, but you were unable to reach them through the thick layer of ice surrounding them".format(victim_id),user_channel,True)

    answer = Mailbox()
    db_set(user_id,'uses',uses - 1)

    if victim_role in ['Cursed Civilian','Sacred Wolf']:
        answer.msg("Your powers' results were **positive**. They are no longer cursed civilians or sacred wolves!",user_channel)
        answer.log("The **Priestess** <@{}> has purified the **{}** <@{}>.".format(user_id,victim_role,victim_id))
        if victim_role == 'Cursed Civilian':
            db_set(victim_id,'role','Innocent')
            answer.dm(rolestory.to_innocent(victim_id,'Cursed Civilian'),victim_id)
        if victim_role == 'Sacred Wolf':
            db_set(victim_id,'role','Werewolf')
            answer.dm("This message yet needs to be written!",victim_id) # TODO
    elif victim_role in ['Innocent','Werewolf']:
        answer.msg("Your powers' results were **neutral**. They were already innocent or a werewolf!",user_channel)
        answer.log("The **Priestess** <@{}> has attempted to purify the **{}** <@{}>.".format(user_id,victim_role,victim_id))
    else:
        answer.msg("Your powers' results were **negative**. They weren't cursed civilians or sacred wolves, so they couldn't be purified!",user_channel)
        answer.log("The **Priestess** <@{}> has ineffectively attempted to purify the **{}** <@{}>.".format(user_id,victim_role,victim_id))

    return answer

# Flute Player
def enchant(user_id,victim_id):
    """This function allows the flute player to enchant targets.
    The function assumes both players are participants, of which the casting user is a flute player. Make sure to have filtered this out already.
    The function returns a Mailbox.

    Keyword arguments:
    user_id -> the flute player who enchants the player
    victim_id -> the player who's enchanted"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to enchant anyone!",True)

    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))

    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))
    victim_enchanted = int(db_get(victim_id,'enchanted'))

    if db_get(victim_id,'role') == 'Flute Player':
        return Mailbox().msg("You cannot enchant a flute player, sorry.",user_channel,True)
    if victim_abducted == 1:
        return Mailbox().msg("You wanted to warm up <@{}>... but you weren't able to find them! That is strange...",user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("You failed to enchant your target, as they were frozen to the bone!.",user_channel,True)
    if victim_enchanted == 1:
        return Mailbox().msg("I am terribly sorry, but you cannot enchant a player who already *IS* enchanted!",user_channel,True)

    answer = Mailbox().msg("You have successfully enchanted <@{}>!".format(victim_id),user_channel)
    db_set(user_id,'uses',uses - 1)

    if user_undead == 1:
        answer.dm("You're an Undead, so you can't actually enchant anyone... but this will help you keep up your cover!",user_id)
        answer.log("The **Undead** <@{}> has pretended to enchant <@{}>.".format(user_id,victim_id))
    else:
        for channel_id in db.get_secret_channels('Flute_Victims'):
            answer.edit_cc(channel_id,victim_id,1)
            answer.msg("<@{}> has been enchanted! Please welcome them to the circle of the enchanted ones.".format(victim_id),channel_id)
        answer.log("The **Flute Player** <@{}> has enchanted <@{}>.".format(user_id,victim_id))
        db_set(victim_id,'enchanted',1)

    return answer

# Ice King
def freeze(user_id,victim_id = None,role = None):
    """This function allows the ice king to add a user to their list of potential freezers, or possibly remove one.
    The function assumes both players are participants, so make sure to have filtered this out already.
    The function returns a Mailbox.

    Keyword arguments:
    user_id -> the ice king's id
    victim_id -> the guessed one's id
    role -> the role they were guessed as. (None if removing the guessed one)"""

    user_channel = int(db_get(user_id,'channel'))

    if victim_id == None:
        if db.get_freezers(user_id) == []:
            return Mailbox().respond("**INVALID SYNTAX:**\nPlease make sure to mention a user.\n\n**Tip:** You can also mention their emoji!",True)

        msg = "__Your current guesses:__\n"
        for freezer in db.get_freezers(user_id):
            msg += "{}. <@{}> - {}\n".format(db_get(freezer[0],'emoji'),freezer[0],freezer[1])
        return Mailbox().msg(msg,user_channel,True)

    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    # tODO: Prevent ice kings from guessing another ice kings (or themselves).
    if victim_abducted == 1:
        return Mailbox().msg("You tried to freeze <@{}>... but you couldn't find them! That is strange.".format(victim_id),user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("You don't need to freeze <@{}>, you silly! They're already frozen!".format(victim_id),user_channel,True)

    if role == None:
        if db.delete_freezer(user_id,victim_id) == True:
            return Mailbox().msg("You have removed <@{}> from your freeze list.".format(victim_id),user_channel,True)
        return Mailbox().msg("**INVALID SYNTAX:** No role provided!\n\nMake sure to provide with a role to add a user to your freeze list.",user_channel,True)

    old_role = db.add_freezer(user_id,victim_id,role)

    if old_role == None:
        return Mailbox().msg("You have added <@{}> to your list as the **{}**.".format(victim_id,role),user_channel,True)
    return Mailbox().msg("You have switched <@{}> from the **{}** to the **{}**.".format(victim_id,old_role,role),user_channel,True)

def freeze_all(user_id):
    """This function allows the ice king to potentially freeze all their guessed players.
    The function assumes the ice king is a participant, so make sure to have filtered this out already.
    The function returns a Mailbox.

    Keyword arguments:
    user_id -> the ice king's id"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to submit a freezing list!",True)
    db_set(user_id,'uses',uses - 1)

    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))
    correct = 0
    incorrect = 0

    for frozone in db.get_freezers(user_id):
        if not db.isParticipant(frozone[0]) or int(db_get(frozone[0],'abducted')) == 1:
            db.delete_freezer(user_id,frozone[0])
        elif frozone[1] != db_get(frozone[0],'role'):
            incorrect += 1
        else:
            correct += 1

    if user_undead == 1:
        answer = Mailbox().msg("You have submitted a list that contains {} players. The result was **unsuccessful**. ".format(correct+incorrect),user_channel)
        answer.msg_add("This means that at least one role was incorrect!")
        answer.log("The **Undead** <@{}> has pretended to submit a freeze list.".format(user_id))
        answer.dm("Hey, you're **Undead**, so this list would've failed anyway - but this helps a little to keep up your cover! 😉",user_id)
        return answer

    if incorrect > 0:
        answer = Mailbox().msg("You have submitted a list that contains {} players. The result was **unsuccessful**. ".format(correct+incorrect),user_channel)
        answer.msg_add("This means that at least one role was incorrect!")
        answer.log("The **Ice King** <@{}> has submitted an **unsuccessful** freeze list. ".format(user_id))
        answer.log_add("The list contained {} guesses, of which {} were correct.".format(incorrect+correct,correct))
        return answer

    # This will execute if all users on the list are correct.
    answer = Mailbox().msg("You have submitted a list that contains {} players. The result was **successful**!\n".format(correct),user_channel)
    if correct > 4:
        answer.msg_add("Congratulations! You guessed them all correctly! ").msg_react('🎉')
    answer.msg_add("Your guessed users will now be frozen.")

    for supersuit in db.get_freezers(user_id):
        db.delete_freezer(user_id,supersuit[0])
        answer.freeze(supersuit[0])

    return answer

# Crowd Seeker
def seek(user_id,victim_id,role):
    """This fuction allows the crowd seeker to inspect players.
    The function assumes the player is a participant and has the correct role, so make sure to have filtered this out already.
    The function returns a Mailbox.

    user_id -> the player who casts the spell
    victim_id -> the player upon whom the spell is cast
    role -> the role the player will be checked as"""

    uses = int(db_get(user_id,'uses'))
    if uses < 1:
        return Mailbox().respond("I am sorry! You currently don't have the ability to seek anyone!",True)

    user_channel = int(db_get(user_id,'channel'))
    user_undead = int(db_get(user_id,'undead'))

    victim_role = db_get(victim_id,'role')
    victim_frozen = int(db_get(victim_id,'frozen'))
    victim_abducted = int(db_get(victim_id,'abducted'))

    if user_undead == 1:
        return Mailbox().dm("I am sorry! You are undead, meaning you can no longer seek players!",user_id,True)
    if victim_abducted == 1:
        return Mailbox().msg("You appear to be unable to find <@{}> among the crowds! Where could they be?".format(victim_id),user_channel,True)
    if victim_frozen == 1:
        return Mailbox().msg("<@{}> was isolated from the crowd, and has gotten too cold to seek. Please try someone else!".format(victim_id),user_channel,True)

    db_set(user_id,'uses',uses - 1)
    answer = Mailbox()

    if role == victim_role:
        answer.msg("{} - <@{}> has the role of the **{}**!".format(db_get(victim_id,'emoji'),victim_id,role),user_channel)
        answer.log("The **Crowd Seeker** <@{}> has seen <@{}> as the **{}**!".format(user_id,victim_id,role))
    else:
        answer.msg("{} - <@{}> does **NOT** have the role of the **{}**.".format(db_get(victim_id,'emoji'),victim_id,role),user_channel)
        answer.log("The **Crowd Seeker** <@{}> guessed incorrectly that <@{}> would be the **{}**.".format(user_id,victim_id,role))

    if uses - 1 > 0:
        answer.msg("You can seek **{}** more time".format(uses-1),user_channel,True)
        if uses - 1 > 1:
            answer.msg_add("s")
        answer.msg_add("!")
    else:
        answer.msg("That\'s it for today! You cannot seek any more players.",user_channel,True)

    return answer

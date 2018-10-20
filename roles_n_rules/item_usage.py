from main_classes import Mailbox
from interpretation import check
from management import db, inventory

def todo(user_id):
    return Mailbox().dm("I am terribly sorry! You cannot use this item yet, because it hasn't been implemented yet!",user_id,True)

def use_item(item_code,message):
    user_id = message.author.id
    if not inventory.has_item(user_id,item_code):
        return Mailbox().dm("I'm sorry. You do not have the correct item in your inventory!",user_id,True)

    # Invisibility cloak
    if item_code == 100:
        if not db.isParticipant(user_id):
            return Mailbox().dm("You are not a participant! You cannot protect yourself if you're not playing.",user_id,True)
        
        db.db_set(user_id,'sleepingover',1)
        inventory.give_item(user_id,100,-1)
        return Mailbox().dm("You are protected for the night. No-one should be able to find you...",user_id).log("<@{}> has used an invisibility cloak to protect themselves for the night!".format(user_id))
    
    # Bucket of water
    if item_code == 101:
        if not db.isParticipant(user_id):
            return Mailbox().dm("You are not a participant! You cannot unpowder yourself if you're not playing.",user_id)

        inventory.give_item(user_id,101,-1)
        answer = Mailbox().dm("The bucket of water refreshed your senses. If you were powdered, this effect has been undone!",user_id)
        if int(db.db_get(user_id,'powdered')) == 1:
            answer.log("<@{}> has used a bucket of water. They are no longer powdered!".format(user_id))
        else:
            answer.log("<@{}> has used a bucket of water - they weren't powdered, however.".format(user_id))
        db.db_set(user_id,'powdered',0)
        return answer
    
    # Royal sword
    if item_code == 102:
        # TODO
        return todo(user_id)

    # Disguise
    if item_code == 103:
        if not db.isParticipant(user_id):
            return Mailbox().dm("You are not a participant! You cannot disguise anyone if you're not playing.",user_id,True)

        role = check.roles(message,1)
        if not role:
            return Mailbox().dm("**INVALID SYNTAX:** No role provided! Please provide a role!",user_id,True)

        victim_id = check.users(message,1,True,True)
        if not victim_id:
            victim_id = [user_id]
        victim_id = victim_id[0]

        user_role = db.db_get(user_id,'role')

        victim_role = db.db_get(victim_id,'role')
        victim_frozen = int(db.db_get(victim_id,'frozen'))
        victim_abducted = int(db.db_get(victim_id,'abducted'))

        if victim_abducted == 1:
            return Mailbox().dm("After having finished your great disguise, it seems like you couldn\'t find your target! Where have they gone off to?",user_id,True)
        if victim_frozen == 1:
            return Mailbox().dm("I am sorry, but <@{}> is too cold for that! You\'ll need a lot more than warm suit to get \'em warmed up.".format(victim_id),user_id,True)

        db.db_set(victim_id,'fakerole',role)
        inventory.give_item(user_id,103,-1)
        answer = Mailbox().dm("You have successfully disguised <@{}> as the **{}**!".format(victim_id,role),user_id)

        answer.log("With a disguise from their inventory, **{}** <@{}> has disguised <@{}>, the **{}**, as the **{}**!".format(user_role,user_id,victim_id,victim_role,role))
        if victim_role == role:
            answer.log_add("\n...does that sound stupid? *Of course!* But how are they supposed to know?")
        return answer
    
    # Name tag
    if item_code == 104:
        # TODO
        return todo(user_id)
    
    # Med kit
    if item_code == 105:
        pass

    # Dagger
    if item_code == 106:
        if not db.isParticipant(user_id):
            return Mailbox().dm("You are not a participant! You cannot attack anyone if you're not playing.",user_id,True)

        if user_id == victim_id:
            return Mailbox().respond("I am sorry, but you cannot attempt suicide!\nNot because it's not an option, no, just because we want to see you SUFFER!",True)

        if int(db.db_get(victim_id,'abducted')) == 1:
            return Mailbox().respond("You attempted to attack <@{}>... but they don't seem to be around in town! That is strange.".format(victim_id),True)
        if int(db.db_get(victim_id,'frozen')) == 1:
            return Mailbox().respond("You wanted to pay a visit to <@{}>... but it seems they were frozen! Try again, please.".format(victim_id),True)

        inventory.give_item(user_id,106,-1)
        db.add_kill(victim_id,'Assassin',user_id)

        answer = Mailbox().dm("You have successfully used a **Dagger** to assasinate <@{}>. They will die when the time shifts!",user_id,True)
        return answer.log("<@{}> has used a **Dagger** to assassinate <@{}>.".format(user_id,victim_id))
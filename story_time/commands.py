import random

def kill_acceptance(victim_id):
    msg_table = []

    msg = "Alright! You have chosen to pay <@{}> a visit tonight...".format(victim_id)
    msg_table.append(msg)

    msg = "Very well, then... <@{}>, it is!".format(victim_id)
    msg_table.append(msg)

    msg = "As you wish. <@{}> will have an unexpected meeting with you tonight.".format(victim_id)
    msg_table.append(msg)

    msg = "Excellent! Got that written down, you\'ll see the results tomorrow."
    msg_table.append(msg)

    msg = "<@{}> shall be visited. Whaddaya think, will they expect it?".format(victim_id)
    msg_table.append(msg)

    msg = "<@{}> better prepare themselves, for you will visit them tonight!".format(victim_id)
    msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table)-1)]

def cc_goodbye(victim_id):
    msg_table = []

    msg = "See ya, <@{}>!".format(victim_id)
    msg_table.append(msg)

    msg = "Bye, <@{}>!".format(victim_id)
    msg_table.append(msg)

    msg = "See you later, <@{}>!".format(victim_id)
    msg_table.append(msg)

    msg = "Noooo, not <@{}>! Did you really have to remove them?".format(victim_id)
    msg_table.append(msg)

    msg = "So long, partner <@{}>. So long.".format(victim_id)
    msg_table.append(msg)

    msg = "Ah, <@{}>\'s gone? About time.".format(victim_id)
    msg_table.append(msg)

    msg = "<@{}> came here to chew gum and kick ass - and it looks like they were out of ass too!".format(victim_id)
    msg_table.append(msg)

    msg = "<@{}>'s gone!".format(victim_id)
    msg_table.append(msg)

    msg = "Got any problems with <@{}>? They\'re solved now.".format(victim_id)
    msg_table.append(msg)

    msg = "Aight! <@{}>'s gone.".format(victim_id)
    msg_table.append(msg)

    msg = "Boom. No more <@{}> here.".format(victim_id)
    msg_table.append(msg)

    msg = "Does it smell like wolf? Well, it *doesn\'t* smell like <@{}> in here anymore.".format(victim_id)
    msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table) - 1)]

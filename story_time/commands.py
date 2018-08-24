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

def cc_welcome(victim_id):
    msg_table = []

    msg = "<@{}> spotted! Agents, report!\n'Clear', 'Clear!', 'Clear.'\n\n*Run, **The Secret Show**.*".format(victim_id)
    msg_table.append(msg)

    msg = "Looks like <@{}> wants to join the party. Well here they are.".format(victim_id)
    msg_table.append(msg)

    msg = "Better late than never! Welcome to the club, <@{}>!".format(victim_id)
    msg_table.append(msg)

    msg = "Who let the dogs out? Ah, <@{}> did! No wonder they were late.".format(victim_id)
    msg_table.append(msg)

    msg = "Hmmm... does anyone smell any updog? Then you\'re probably a wolf! <@{}>, quick, come and get them!".format(victim_id)
    msg_table.append(msg)

    msg = "Oh, yeah. Almost forgotten that <@{}> needs to be in here too! Hey, hi, how ya doin'?".format(victim_id)
    msg_table.append(msg)

    msg = "Oh... do you really want me to add <@{}>?\nAre you *sure*?".format(victim_id)
    msg_table.append(msg)

    msg = "**YES!** I was hoping you'd ask me to add <@{}>!".format(victim_id)
    msg_table.append(msg)

    msg = "Well, look who's here! My favourite Discord user! Hey there, <@{}>!".format(victim_id)
    msg_table.append(msg)

    msg = "Wait, you wanna add <@{}>, too? But what if you run out of food?\nOr.... *ARE* they the food?".format(victim_id)
    msg_table.append(msg)

    msg = "What does the fox say?\n<@{0}> <@{0}> <@{0}> <@{0}> <@{0}> <@{0}>".format(victim_id)
    msg_table.append(msg)

    msg = "Mmmm, it looks like a fun party in here! No doubt that <@{}> shall feel welcome in here.".format(victim_id)
    msg_table.append(msg)

    msg = "I can't pull a rabbit out of my hat, but I can get <@{0}> in here! Welcome, <@{0}>!".format(victim_id)
    msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table) - 1)]

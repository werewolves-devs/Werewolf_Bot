def channel_introduction(role):

    # Do it like this:
    if role == "Assassin":
        # End lines with a \ if you do not actually want a new line to start
        msg = """\
**=========================**
**WELCOME, ASSASSIN**
**=========================**
This town is like an old kitchen... it's a giant mess. Luckily, the town has *you*, \
their protector, who picks out the cockroaches for them and squishes them like the puny animals they are. 
You do not exactly know what is about to happen, but your senses never lie; \
something *TERRIBLE* is happening, and it depends on your actions how much the town will suffer from it!
You do not know your allies, your masters taught you never to trust anyone. However, \
you fear you can't do this alone. You must find the ones to save, and especially the ones to kill.
**You are the assassin. Each night (except for the first one), you can attack and kill a player you suspect.\
Play the game whichever way you'd like, but try to keep the innocents alive. Good luck.**\
"""    
    if role == "Aura Teller":
        msg = """\
**=========================**
**WELCOME, AURA TELLER**
**=========================**
Not everyone in this town can be trusted - and you can feel it! You sense it in the people among you, \
some have a... smell of evil around them. It is time to find out who is to be trusted, and who has solemnly \
sworn to be up to no good!
**You are the Aura Teller. Each night, you may inspect a player and find out if they are part of the wolf pack.\
Remember that a positive aura does not necessarily mean they are on your team! Good luck.**\
"""
    
    if role == "Baker":
        msg = """\
**=========================**
**WELCOME, BAKERS**
**=========================**
As it is crucial that the bread is distributed evenly among the town, you have a trusted league with each other. \
You all know each other well enough, and can be sure to count on each other. \
Let's hope that the rest of the town is trustworthy as well...
**You are the bakers. All other members of this channel are bakers. Assuming their roles do not change, you can trust them completely.\
Use this group to share information, plan strategies and catch liars! Good luck.**\
"""
    
    # Ignore this. This allows us to see your message.
    return msg

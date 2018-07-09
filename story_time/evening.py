import random

def evening(victim,actual_victim):
    msg_table = []

    if victim == actual_victim:
        msg = '''This works basically the same as evening.py \
<@{0}> is getting lynched if the victim is equal to the actual victim. \
I\'d suggest focusing on this one mostly, for this is the most common scenario.'''.format(victim)
        msg_table.append(msg)
    
    if actual_victim == '':
        msg = '''Though this isn\'t a very common scenario, it\'s not rare either. \
Stories for this one should be like a plot twist. What happens in these scenarios, \
is that for some reason <@{0}> wasn't lynched, even though that was the idea. \
The reason it fails is kinda mysterious, so make the cause have strange things; \
the rope broke when trying to hang them, they couldn't get a fire to burn them on, \
when trying to drown them in the town's well, they kept floating, the king forbid their death, etc.'''.format(victim)
        msg_table.append(msg)
    
    if victim != actual_victim:
        msg = '''This is a very rare scenario, but also a huge plot twist! In these cases,
people die while others were supposed to. These are huge plot twists, but don\'t focus on them \
TOO much given their frequency.'''
        msg_table.append(msg)
    
    return msg_table[random.randint(0,len(msg_table)-1)]

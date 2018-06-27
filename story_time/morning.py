import random

def story_time(victims):
    amount = len(victims)
    msg_table = []

    if amount == 0:
        msg = '''This can be any story! Funny no-one died!'''
        msg_table.append(msg)

    if amount == 0:
        msg = '''Another story! Yay'''
        msg_table.append(msg)
    
    if amount == 0:
        msg = '''You can just add an enter to the story!
There! That works just fine! Don\'t worry about how ugly it looks. ;)

Oh, also, if the line\'s getting too thick and you want to write on a \
new line without actually having the story start on a new line, put a \
slash at the end of the line.

You don\'t HAVE to do that, though. I\'d suggest writing this story elsewhere, where you are comfortable writing stuff. Then you could just copypaste it here, and it\'s totally fine if you make the lines unbearably long. If some programmers start complaining, that\'s their problem, not yours.
Also, as you probably have noticed, if you want the apostrophe, type a backslash in front; don\'t forget!'''
        msg_table.append(msg)
    
    if amount == 1:
        msg = '''Oh no! A story where <@{0}> died!'''.format(victims[0])
        msg_table.append(msg)
    
    if amount == 2:
        msg = '''Two more people died this morning! Their ids were {0} and {1}, \
but please ping them by typing <@ in front and > behind. \
You can use the number in-between the semi-colons to decide whom you want to mention. This means\
 you can also decide to ping <@{0}> multiple times, if you want. Would <@{0}> enjoy that?'''.format(victims[0],victims[1])
        msg_table.append(msg)
    
    if amount == 4:
        msg = '''Other than that, just copy any code you see, like <@{2}>, <@{0}> \'n\' <@{1}> did.\
Also, don\'t be afraid to ask, but the most important thing is; don\'t be afraid to make mistakes.

The reason we need someone to do it, is because writing the stories takes time; \
fixing any bugs you make will take up WAYYYY less than actually writing it. \
So don\'t worry! We\'re looking forward to your stories, just like <@{3}>. ;)'''.format(victims[0],victims[1],victims[2],victims[3])
        msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table)-1)]

import random

def evening(victims):
    msg_table = []
    amount = len(victims)

    if amount == 0:
        msg = "No-one wanted to die today. Yay!\n"
        msg += "*Written by Randium.*"
        msg_table.append(msg)

        msg = "The town had a few plans for today. They held a public vote, they chose a target, "
        msg += "they prepared the fireplace, and... wait, who was the victim again?\n"
        msg += "The whole town seemed to have forgotten who was to be lynched. Strange! Well, in that case, "
        msg += "I guess no-one died today. Too bad!\n"
        msg += "*Written by Randium.*"
        msg_table.append(msg)

        msg = "Today was a tiring day, a *very* tiring day.\n"
        msg += "So tired, they decided not to lynch anyone.\n\n...\n\nEven telling this story makes me sleepy.\n"
        msg += "*Written by Randium.*"
        msg_table.append(msg)
    
    if amount == 1:
        msg = "Yes, it was clear that the majority voted for <@{0}>. Bye bye!\n".format(victims[0])
        msg += "*Written by Randium.*"
        msg_table.append(msg)
    
        msg = "As <@{}> screamed on top of their lungs, begging for the town not to chop their head off, lightning struck ".format(victims[0])
        msg += "a tree besides <@{0}>. The tree fell on top of them. *\"<@{0}> died from a tree\"* is written on their tombstone.\n".format(victims[0])
        msg += "*Written by dayy.*"
        msg_table.append(msg)

        msg = "<@{}>, with tears in their eyes, begged for the town not to punish them. "
        msg += "Their cries were in vain, for the Participants did not listen. ".format(victims[0])
        msg += "At the very least, they were put out of their misery much more quickly since they were out of breath.\n"
        msg += "*Written by BlueGlues.*"

    if msg_table == []:
        msg = "Oof, lots of people died.\nThen this is a great moment to make an advertisement, @everyone!\n\n"
        msg += "Don't you think too the bot lacks a bit of storytime? So do we! Please, help us by writing something "
        msg += "that could be said here instead of this annoying ping!\n"
        msg += "*Written by Randium.*"
        msg_table.append(msg)
    
    return msg_table[random.randint(0,len(msg_table)-1)]

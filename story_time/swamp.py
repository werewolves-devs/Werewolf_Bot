import random

def kidnap():
    msg_table = []

    msg = """How unfortunate!
    Last night, you were starving and you felt like the world would end if you didn\'t get anything to eat! \
    That\'s when you decided to go into the forest and find some berries.
    You weren't unsuccesful, but the way home seemed far longer than the path used to be. As the path is taking \
    longer and longer, you\'re starting to think you got lost! That\'s when you meet the others, who seemed to be lost as well.
    One of them is talking about some ruins they found, about an ancient monster slumbering in the forest, trying to kill you all!
    **You have been abducted by The Thing. You can only have contact with the other abducted players. One player secretly \
    has contact with the outside. That player is The Thing. Kill them to be set free again.**"""
    msg_table.append(msg)

    msg = """Yesterday was a relatively pleasant day. The execution was a wild one! In the evening, while on your way home, \
    you saw a silhouette in the bushes, waving at you. Confused by what it could mean, *(does someone wish to talk to you in private? \
    Another conspiracy channel?)* you follow the silhouette into the forest. Once you reach the swamp, you lose the \
    human-like figure, and you only see the shadow of a deer staring right at you.
    Confused and lightly spooked out in the dark forest, you turn around and start to walk back, but you cannot find your way home \
    in the darkness! After a few hours, you stumble upon other people who claim to be lost in the woods, all talking about a strange \
    creature they had seen in the distance...
    **You have been abducted by The Thing. You can only have contact with the other abducted players. One player secretly \
    has contact with the outside. That player is The Thing. Kill them to be set free again.**"""
    msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table)-1)]

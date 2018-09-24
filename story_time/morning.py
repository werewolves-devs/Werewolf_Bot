import random

# TODO: Add Mayor / Reporter / Guardian Stories
# The Participants rejoiced as $Voted was elected mayor. Some held their suspicions against them, but despite the tension, the villagers proceeded to have a wonderful time at the tavern congratulating the newly-made leader.

# TODO: Add Random-Player Inclusions
#

# Aviable Types:
#   Inactive
#   Cupid
#   Wager
#   Zombie
#   Lynch
#   Barber
#   Hooker
#   Executioner
#   Huntress
#   Assassin
#   Cult
#   Priest
#   Witch
#   Werewolf
#   Demon
#   Horseman
#   Pyromancer

messages = [
    ("Werewolf", "Regicide", "Light had begun to shine through the village, when the whole town heard something almost like the sound of sticks snapping in a strong wind. With curiosity, they emerged from their houses, only to find the horrible hawed and mangled body of {0}. What kind d of creature could have done such a thing?"),
    ("Inactive", "Regicide", "{0} jumped off a cliff and attempted to fly, only to remember that he didn't have wings."),
    ("Pyromancer", "BlueGlues", "As the sun rose, a faint crackling was heard across town. The houses of {0}, {0} and {0}, much to the Participants' dismay, were the source of the sound--all that remained were some burnt wooden boards, hot pieces of metal, and ashes. The smell of charred flesh that lingered around the site was unnerving--for the Participants knew who it belonged to."),
    ("Lynch", "BlueGlues", "{0}, with tears in their eyes, begged for the town not to punish them. Their cries were in vain, for the Participants did not listen. At the very least, they were put out of their misery much more quickly since they were out of breath."),
    ("Pyromancer", "Regicide", "It was around midnight when everyone awoke. In the town square they found the body of {0} smoldering on wooden stakes. By their feet was a charred drawing of a middle finger. Who killed these poor souls? There was only one way to find out."),
    ("Assassin", "BlueGlues", "A body was discovered slumped against one of the Participants' houses--more precisely, the body of {0}. Further inspection of the corpse revealed a thin, clean cut across the victim's throat--as if the one who killed them was experienced in their craft. Had it not been for the blood, no one would have noticed the wound."),
]


def ChooseRandom(reason):
    s = [msg for msg in messages if msg[0] == reason]
    if s is None | len(s) == 0:
        return None
    return s[random.randint(0, len(messages)-1)]


def story_time(victims):
    amount = len(victims)
    msg_table = []

    if amount == 0:
        return 'No-one died last night. Yay!'


    workString = ""
    authorsString = "*Thanks to: "
    try:
        for victim in victims:
            userId = victim[0]
            reason = victim[1]

            res = ChooseRandom(reason)
            if res is None:
                raise Exception("Coudnt Get Message for Reason: \"{0}\"".format(reason))

            workString += res[2]
            workString += "\n\n"
            authorsString += res[1] + ", "

        # Remove the last ", ", and add a "."
        authorsString = authorsString[:-2]
        authorsString += ".*"


        return workString + authorsString
    except Exception as ex:
        pass # We dont care, well go on with the Fallback, this
             # isnt the nicest, i know, but better then a plain return.


    #Fallback, in case of not found message

    # Story written by TROPICALCYCLONEALERT
    if amount == 1:
        msg = '''A wispy wind billowed throughout the night. '\
        Dawn was quickly approaching, and only the slightest amount of townsfolk were coming around. \
        As the sun rose over the distant horizon, the first villagers ventured out of the safety of their homes.  
        Soon enough, a dog began to bark. Its owner quickly came over to calm it down. The dog did not stop, \
        and walked towards a corner. The tall animal came to a halt, and beckoned its owner to come. \
        The owner was appalled by the sight. The brick walls were imbued with the dark stain of blood, \
        and a decapitated head was at the base.  
        A few paces away, a foot was found. Forty feet later, another foot and a hand was found. \
        The man who had discovered the dismembered corpse acknowledged the presence of a particular smell, \
        much like that of a wolf that occasionally prowled along the edges of the forests. \
        An autopsy done by the town surgeon revealed a wolf tooth ingrained within the skull. \
        The corpse was revealed to be of one <@{0}>.'''.format(victims[0])
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 3:
        msg = '''Loud seaguls bellowed at dawn, waking the townsfolk to an eerie atmosphere. \
        The gray clouded sky silhouetted carrion birds circling the town with loud cawing, \
        adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. \
        A corpse was leaning towards the doorframe.  
        It was <@{0}> with their eyes being completely pecked by crows! A short time after the corpses of \
        <@{1}> and <@{2}> were discovered strewn across the town square. \
        Will this just be the appetiser?'''.format(victims[0],victims[1],victims[2])
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 4:
        msg = '''Loud seaguls bellowed at dawn, waking the townsfolk to an eerie atmosphere. \
        The gray clouded sky silhouetted carrion birds circling the town with loud cawing, \
        adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. \
        A corpse was leaning towards the doorframe.  
        It was <@{0}> with their eyes being completely pecked by crows! A short time after the corpses of <@{1}>, \
        <@{2}> and <@{3}> were discovered strewn across the town square. \
        Will this just be the appetiser?'''.format(victims[0],victims[1],victims[2],victims[3])
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 5:
        msg = '''Loud seaguls bellowed at dawn, waking the townsfolk to an eerie atmosphere. \
        The gray clouded sky silhouetted carrion birds circling the town with loud cawing, \
        adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. \
        A corpse was leaning towards the doorframe.  
        It was <@{0}> with their eyes being completely pecked by crows! A short time after the corpses of <@{1}>, \
        <@{2}>, <@{3}> and even <@{4}> were discovered strewn across the town square. \
        Will this just be the appetiser?'''.format(victims[0],victims[1],victims[2],victims[3],victims[4])
        msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table)-1)]

if __name__ == '__main__':
    print(story_time([237894723]))

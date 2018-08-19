import random

def morning(victims): #make consistent to "evening", if there are no dependencies?
    amount = len(victims)
    msg_table = []

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
The corpse was revealed to be of one {0}.'''.format(victims[0])
        msg_table.append(msg)

        msg = '''Dawn came, and the townsfolk woke up, too tired to speak.\
There had been much noise during the night, and the first awaken went to investigate.\
Finding a trail of blood on the streets of the village, they followed it to a horrifiying sight!\
In a dark alley in the town, there was a corpse of a villager, dragged through the village.\
After a lenghtly investigation, the townfolk finally discovered it was <@{0}>!\
The townsfolk wondered who would have done this,\
but then the cries of a wolf in the nearby woods left no doubts in their minds.\
Who will be next?'''.format(victims[0])
        msg_table.append(msg)

    if amount == 2:
        msg = '''The townsfolk woke up to a fine day.\
Nothing bad had happened, and everything was normal. But then, two villagers' absence was noted, <@{0}> and <@{1}>!
The villager who looked for them discovered something terrible had happened!\
The body parts of the people were thrown into the village well, whose water had turned red with blood.\
After careful investigation, the townsfolk determined that it happened just last night, as they had fetched water the day before.
What will happen next?'''.format(victims[0], victims[1])
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 3:
        msg = '''Loud seaguls bellowed at dawn, waking the townsfolk to an eerie atmosphere. \
The gray clouded sky silhouetted carrion birds circling the town with loud cawing, \
adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. \
A corpse was leaning towards the doorframe. \
It was <@{0}> with their eyes being completely pecked by crows! A short time after the corpses of \
<@{1}> and <@{2}> were discovered strewn across the town square. \
Will this just be the appetiser?'''.format(victims[0],victims[1],victims[2])
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 4:
        msg = '''Loud seaguls bellowed at dawn, waking the townsfolk to an eerie atmosphere. \
The gray clouded sky silhouetted carrion birds circling the town with loud cawing, \
adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. \
A corpse was leaning towards the doorframe. \
It was <@{0}> with their eyes being completely pecked by crows! A short time after the corpses of <@{1}>, \
<@{2}> and <@{3}> were discovered strewn across the town square. \
Will this just be the appetiser?'''.format(victims[0],victims[1],victims[2],victims[3])
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 5:
        msg = '''Loud seaguls bellowed at dawn, waking the townsfolk to an eerie atmosphere. \
The gray clouded sky silhouetted carrion birds circling the town with loud cawing, \
adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. \
A corpse was leaning towards the doorframe. \
It was <@{0}> with their eyes being completely pecked by crows! A short time after the corpses of <@{1}>, \
<@{2}>, <@{3}> and even <@{4}> were discovered strewn across the town square. \
Will this just be the appetiser?'''.format(victims[0],victims[1],victims[2],victims[3],victims[4])
        msg_table.append(msg)

    return msg_table[random.randint(0,len(msg_table)-1)]

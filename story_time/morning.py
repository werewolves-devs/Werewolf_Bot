import random

def story_time(victims):
    amount = len(victims)
    msg_table = []

    if amount == 0:
        return 'No-one died last night. Yay!'

    # Story written by TROPICALCYCLONEALERT
    if amount == 1:
        msg = "A wispy wind billowed throughout the night. "
        msg += "Dawn was quickly approaching, and only the slightest amount of townsfolk were coming around. "
        msg += "As the sun rose over the distant horizon, the first villagers ventured out of the safety of their homes.\n"
        msg += "Soon enough, a dog began to bark. Its owner quickly came over to calm it down. The dog did not stop, "
        msg += "and walked towards a corner. The tall animal came to a halt, and beckoned its owner to come. "
        msg += "The owner was appalled by the sight. The brick walls were imbued with the dark stain of blood, "
        msg += "and a decapitated head was at the base.\n"
        msg += "A few paces away, a foot was found. Forty feet later, another foot and a hand was found. "
        msg += "The man who had discovered the dismembered corpse acknowledged the presence of a particular smell, "
        msg += "much like that of a wolf that occasionally prowled along the edges of the forests. "
        msg += "An autopsy done by the town surgeon revealed a wolf tooth ingrained within the skull. "
        msg += "The corpse was revealed to be of one <@{}>.\n".format(victims[0])
        msg += "*Written by TROPICALCYCLONEALERT.*"
        msg_table.append(msg)

        msg += "The sound of a whistling kettle broke the dawn for <@{}>'s neighbour as they prepared their morning ".format(victims[0])
        msg += "pick-me-up coffee. To their discontent, the cofee tin had naught but a bean left.\n"
        msg += "*\"Rats thumbs are afoot,\" the shouted, and wrathfully stumbled outside to their neighbour, <@{}>.* ".format(victims[0])
        msg += "After banging on the door with no luck, the neighbour attempted to open the door. The morning sun "
        msg += "shined a beam of light into the room as the door creaked open. Out of the shadow a bloody hand "
        msg += "beloning to <@{}>, was revealed.\nThe bag of coffeee had been soiled by the dark acts that ".format(victims[0])
        msg += "transpired that night.\n*Written by Kudels.*"
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 3:
        msg = "Loud seagulls bellowed at dawn, waking the townsfolk to an eerie atmosphere. "
        msg += "The gray clouded sky silhouetted carrion birds circling the town with loud cawing, "
        msg += "adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. "
        msg += "A corpse was leaning towards the doorframe.\n"
        msg += "It was <@{}> with their eyes being completely pecked by crows! A short time after, the corpses of ".format(victims[0])
        msg += "<@{}> and <@{}> were discovered strewn across the town square. ".format(victims[1],victims[2])
        msg += "Will this just be the appetiser?\n"
        msg += "*Written by Kudels.*"
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 4:
        msg = "Loud seagulls bellowed at dawn, waking the townsfolk to an eerie atmosphere. "
        msg += "The gray clouded sky silhouetted carrion birds circling the town with loud cawing, "
        msg += "adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. "
        msg += "A corpse was leaning towards the doorframe.\n"
        msg += "It was <@{}> with their eyes being completely pecked by crows! A short time after, the corpses of <@{}>,".format(victims[0],victims[1])
        msg += "<@{}> and <@{}> were discovered strewn across the town square. ".format(victims[2],victims[3])
        msg += "Will this just be the appetiser?\n"
        msg += "*Written by Kudels.*"
        msg_table.append(msg)

    # Story written by Kudels
    if amount == 5:
        msg = "Loud seagulls bellowed at dawn, waking the townsfolk to an eerie atmosphere. "
        msg += "The gray clouded sky silhouetted carrion birds circling the town with loud cawing, "
        msg += "adding to the hellscape athmosphere. The first villager to open their doors discovered something horrific. "
        msg += "A corpse was leaning towards the doorframe.\n"
        msg += "It was <@{}> with their eyes being completely pecked by crows! A short time after, the corpses of <@{}>,".format(victims[0],victims[1])
        msg += "<@{}>, <@{}> and even <@{}> were discovered strewn across the town square. ".format(victims[2],victims[3],victims[4])
        msg += "Will this just be the appetiser?\n"
        msg += "*Written by Kudels.*"
        msg_table.append(msg)

    if msg_table == []:
        msg_table.append("Lots of peeps died! Oh no!")

    return msg_table[random.randint(0,len(msg_table)-1)]

if __name__ == '__main__':
    print(story_time([237894723]))

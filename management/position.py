roles_list = ["Innocent","Alcoholic","Amulet Holder","Assassin","Aura Teller","Baker","Butcher","Barber","Crowd Seeker",
"Cult Leader","Cult Member","Cupid","Cursed Civilian","Dog","Executioner","Exorcist","Fortune Teller","Fortune Apprentice",
"Grandma","Hooker","Huntress","Idiot","Innkeeper","Jack Robinson","Look-Alike","Macho","Mad Scientist","Priest","Priestess",
"Raven","Robin Jackson","Royal Knight","Runner","Town Elder","Witch","Werewolf","Bloody Butcher","Curse Caster","Hell Hound",
"Infected Wolf","Lone Wolf","Sacred Wolf","Tanner","Warlock","White Werewolf","Wolf's Cub","Angel","Despot","Devil","Demon",
"Flute Player","Horseman","Ice King","Immortal","Psychopath","Pyromancer","The Thing","Undead","Vampire","Zombie"]

wolf_pack = ["Werewolf","Bloody Butcher","Hell Hound","Infected Wolf","Sacred Wolf","White Werewolf","Wolf's Cub"]

villager_team = ["Innocent","Alcoholic","Amulet Holder","Assassin","Aura Teller","Baker","Butcher","Barber","Crowd Seeker",
"Cult Leader","Cult Member","Cupid","Cursed Civilian","Dog","Executioner","Exorcist","Fortune Teller","Fortune Apprentice",
"Grandma","Hooker","Huntress","Idiot","Innkeeper","Jack Robinson","Look-Alike","Macho","Mad Scientist","Priest","Priestess",
"Raven","Robin Jackson","Royal Knight","Runner","Town Elder","Witch"]
wolf_team = ["Werewolf","Bloody Butcher","Curse Caster","Hell Hound","Infected Wolf","Lone Wolf","Sacred Wolf","Tanner",
"Warlock","White Werewolf","Wolf's Cub"]
solo_team = ["Angel","Despot","Devil","Demon","Flute Player","Horseman","Ice King","Immortal","Psychopath","Pyromancer",
"The Thing","Undead","Vampire","Zombie"]

claimspace_village = ["Innocent","Alcoholic","Cursed Civilian","Runner"]
claimspace_wolf = ["Werewolf","Sacred Wolf"]

personal_secrets = ["Amulet Holder","Assassin","Aura Teller","Barber","Crowd Seeker","Cupid","Dog","Executioner",
"Exorcist","Fortune Teller","Fortune Apprentice","Grandma","Hooker","Huntress","Innkeeper","Look-Alike","Priest",
"Priestess","Raven","Royal Knight","Witch","Curse Caster","Infected Wolf","Lone Wolf","Tanner",
"Warlock","White Werewolf","Devil","Horseman"]

shared_secrets = ["Baker","Butcher","Cult Leader","Werewolf","Hell Hound","Demon","Flute Player",
"Ice King","Psychopath","Pyromancer","The Thing","Undead","Vampire","Zombie"]

pretenders = ["Baker","Butcher","Cult Leader","Cult Member","Werewolf","Bloody Butcher","Hell Hound",
"Infected Wolf","Sacred Wolf","White Werewolf","Wolf's Cub","Flute Player","Ice King","Psychopath","Pyromancer"]



def valid_distribution(role_table,just_checking=False):
    hasVillage = 0
    hasWolf = 0
    hasSolo = 0

    counter_village = 0
    counter_wolf = 0
    counter_solo = 0

    counter_claimspace_village = 0
    counter_claimspace_wolf = 0

    counter_horsemen = 0

    for role in role_table:
        if role in villager_team:
            hasVillage = 1
            counter_village += 1
        if role in wolf_team:
            hasWolf = 1
            counter_wolf += 1
        if role in solo_team:
            hasSolo = 1
            counter_solo += 1
        if role in claimspace_village:
            counter_claimspace_village += 1
        if role in claimspace_wolf:
            counter_claimspace_wolf += 1
        if role == 'Horseman':
            counter_horsemen += 1
    
    # If only one category is available, do not accept the distribution.
    if (hasVillage + hasWolf + hasSolo) < 2:
        return False

    # Special conditions
    if counter_horsemen not in [0,4]:
        return False
    if counter_horsemen == 4 and len(role_table) < 20:
        return False
    if "Cult Member" in role_table and "Cult Leader" not in role_table:
        return False
    if "Demon" in role_table and "Devil" not in role_table:
        return False
    if "Undead" in role_table and "Vampire" not in role_table:
        return False
    if "Innkeeper" in role_table and "Ice King" not in role_table:
        return False
    if "Priestess" in role_table and ("Cursed Civilian" not in role_table and "Sacred Wolf" not in role_table and "Curse Caster" not in role_table):
        return False
    if "Robin Jackson" in role_table and "Jack Robinson" not in role_table:
        return False
    if "Jack Robinson" in role_table and "Robin Jackson" not in role_table:
        return False
    if "Butcher" in role_table and "Bloody Butcher" not in role_table:
        return False
    if "Bloody Butcher" in role_table and "Butcher" not in role_table:
        return False
    if "Fortune Apprentice" in role_table and "Fortune Teller" not in role_table:
        return False

    if just_checking:
        return True

    # Normalizing the values.
    # Note that the function would've already returned False
    # if the list was empty. We cannot divide by zero here.
    counter_village = float(counter_village)/len(role_table)
    counter_wolf = float(counter_wolf)/len(role_table)
    counter_solo = float(counter_solo)/len(role_table)

    answer = "The amount of villagers is... "
    if counter_village == 0:
        answer += "**EMPTY**\n"
    elif counter_village < 0.25:
        answer += "**MARGINAL**\n"
    elif counter_village < 0.333:
        answer += "**SMALL**\n"
    elif counter_village < 0.45:
        answer += "**ACCEPTABLE**\n"
    elif counter_village < 0.55:
        answer += "**OPTIMAL**\n"
    elif counter_village < 0.666:
        answer += "**ACCEPTABLE**\n"
    elif counter_village < 0.75:
        answer += "**HIGH**\n"
    elif counter_village < 0.85:
        answer += "**HUGE**\n"
    elif counter_village < 1:
        answer += "**EXTREME**\n"
    else:
        answer += "an amount that shouldn't be accepted! Inform the Game Masters, please!"

    answer += "The amount of werewolves is... "
    if counter_wolf == 0:
        answer += "**EMPTY**\n"
    elif counter_wolf < 0.1:
        answer += "**MARGINAL**\n"
    elif counter_wolf < 0.2:
        answer += "**SMALL**\n"
    elif counter_wolf < 0.25:
        answer += "**ACCEPTABLE**\n"
    elif counter_wolf < 0.334:
        answer += "**OPTIMAL**\n"
    elif counter_wolf < 0.4:
        answer += "**ACCEPTABLE**\n"
    elif counter_wolf < 0.51:
        answer += "**HIGH**\n"
    elif counter_wolf < 0.6:
        answer += "**HUGE**\n"
    elif counter_wolf < 0.7:
        answer += "**EXTREME**\n"
    elif counter_wolf < 1:
        answer += "**DISPROPORTIONALLY BIG**\n"
    else:
        answer += "an amount that shouldn't be accepted! Inform the Game Masters, please!"
     
    answer += "The amount of solo roles is... "
    if counter_solo == 0:
        answer += "**EMPTY**\n"
    elif counter_solo < 0.2:
        answer += "**SMALL**\n"
    elif counter_solo < 0.25:
        answer += "**ACCEPTABLE**\n"
    elif counter_solo < 0.35:
        answer += "**OPTIMAL**\n"
    elif counter_solo < 0.5:
        answer += "**HIGH**\n"
    elif counter_solo < 0.7:
        answer += "**HUGE**\n"
    elif counter_solo < 1:
        answer += "**EXTREME**\n"
    
    answer += "\nThe claimspace among innocents is "

    if counter_claimspace_village < 3:
        answer += "way too small.\n"
    elif counter_claimspace_village < 5:
        answer += "quite small.\n"
    elif counter_claimspace_village < 8:
        answer += "relatively small.\n"
    elif counter_claimspace_village < 12:
        answer += "healthy.\n"
    elif counter_claimspace_village < 16:
        answer += "quite big.\n"
    else:
        answer += "immense.\n"
    
    if "White Werewolf" in role_table:
        answer += "The claimspace among wolves is "

        if counter_claimspace_wolf == 0:
            answer += "so small, that the white werewolf will be caught alsmost immediately.\n"
        elif counter_claimspace_wolf < 3:
            answer += "awkwardly small.\n"
        elif counter_claimspace_wolf < 6:
            answer += "not very big, though doable.\n"
        elif counter_claimspace_wolf < 8:
            answer += "quite healthy.\n"
        else:
            answer += "big. But that's okay!\n"
    
    return answer


# Converts the required string to its position in the SQLite database.
# Raises an error if it cannot find the string.
def positionof(column):
    if column == "id":
        return 0
    if column == "name":
        return 1
    if column == "emoji":
        return 2
    if column == "activity":
        return 3
    if column == "channel":
        return 4
    if column == "role":
        return 5
    if column == "fakerole":
        return 6
    if column == "uses":
        return 7
    if column == "votes":
        return 8
    if column == "threatened":
        return 9
    if column == "enchanted":
        return 10
    if column == "demonized":
        return 11
    if column == "powdered":
        return 12
    if column == "frozen":
        return 13
    if column == "undead":
        return 14
    if column == "bites":
        return 15
    if column == "bitten":
        return 16
    if column == "souls":
        return 17
    if column == "sleepingover":
        return 18
    if column == "lastwords":
        return 19
    if column == "abducted":
        return 20
    if column == "ccs":
        return 21
    if column == 'horseman':
        return 22
    if column == 'amulet':
        return 23

    raise SyntaxError("Unable to convert \'{}\' to SQLite position.".format(column))

def check_for_int(s):
    """Returns True if the value s is or can be converted to an integer. Returns False otherwise."""
    try:
        int(s)
        return True
    except ValueError:
        return False

# This piece is only run when this is the main file in the terminal.
# It will not run if the file is being imported by another file.
if __name__ == "__main__":

    print(positionof("demonized"))
    print(positionof("bites"))
    print(positionof("id"))
    print(positionof("Something that doesn't exist! :D"))

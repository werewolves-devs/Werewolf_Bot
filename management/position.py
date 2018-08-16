roles_list = ["Innocent","Alcoholic","Amulet Holder","Assassin","Aura Teller","Baker","Butcher","Barber","Crowd Seeker",
"Cult Leader","Cult Member","Cupid","Cursed Civilian","Dog","Executioner","Exorcist","Fortune Teller","Fortune Apprentice",
"Grandma","Hooker","Huntress","Idiot","Innkeeper","Jack Robinson","Look-Alike","Macho","Mad Scientist","Priest","Priestess",
"Raven","Robin Jackson","Royal Knight","Runner","Town Elder","Witch","Werewolf","Bloody Butcher","Curse Caster","Hell Hound",
"Infected Wolf","Lone Wolf","Sacred Wolf","Tanner","Warlock","White Werewolf","Wolf's Cub","Angel","Despot","Devil","Demon",
"Flute Player","Four Horsemen","Ice King","Immortal","Psychopath","Pyromancer","The Thing","Undead","Vampire"," Zombie"]

wolf_pack = ["Werewolf","Bloody Butcher","Hell Hound","Infected Wolf","Sacred Wolf","White Werewolf","Wolf's Cub"]

villager_team = ["Innocent","Alcoholic","Amulet Holder","Assassin","Aura Teller","Baker","Butcher","Barber","Crowd Seeker",
"Cult Leader","Cult Member","Cupid","Cursed Civilian","Dog","Executioner","Exorcist","Fortune Teller","Fortune Apprentice",
"Grandma","Hooker","Huntress","Idiot","Innkeeper","Jack Robinson","Look-Alike","Macho","Mad Scientist","Priest","Priestess",
"Raven","Robin Jackson","Royal Knight","Runner","Town Elder","Witch"]
wolf_team = ["Werewolf","Bloody Butcher","Curse Caster","Hell Hound","Infected Wolf","Lone Wolf","Sacred Wolf","Tanner",
"Warlock","White Werewolf","Wolf's Cub"]
solo_team = ["Angel","Despot","Devil","Demon","Flute Player","Four Horsemen","Ice King","Immortal","Psychopath","Pyromancer",
"The Thing","Undead","Vampire","Zombie"]

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
    if column == "amulets":
        return 19
    if column == "abducted":
        return 20
    if column == "ccs":
        return 21
    if column == 'horseman':
        return 22

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

roles_list = ["Innocent","Alcoholic","Amulet Holder","Assassin","Aura Teller","Baker","Butcher","Barber","Crowd Seeker",
"Cult Leader","Cult Member","Cupid","Cursed Civilian","Dog","Executioner","Exorcist","Fortune Teller","Fortune Apprentice",
"Grandma","Hooker","Huntress","Idiot","Innkeeper","Jack Robinson","Look-Alike","Macho","Mad Scientist","Priest","Priestess",
"Raven","Robin Jackson","Royal Knight","Runner","Town Elder","Witch","Werewolf","Bloody Butcher","Curse Caster","Hell Hound",
"Infected Wolf","Lone Wolf","Sacred Wolf","Tanner","Warlock","White Werewolf","Wolf's Cub","Angel","Despot","Devil","Demon",
"Flute Player","Four Horsemen","Ice King","Immortal","Psychopath","Pyromancer","The Thing","Undead","Vampire"," Zombie"]

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
    if column == "lovers":
        return 18
    if column == "sleepers":
        return 19
    if column == "amulets":
        return 20
    if column == "zombies":
        return 21
    
    raise SyntaxError("Unable to convert \'{}\' to SQLite position.".format(column))

# This piece is only run when this is the main file in the terminal.
# It will not run if the file is being imported by another file.
if __name__ == "__main__":

    print(positionof("demonized"))
    print(positionof("bites"))
    print(positionof("id"))
    print(positionof("Something that doesn't exist! :D"))

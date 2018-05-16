import roles as role

# This function changes a player's role to a given role.
# Make sure the player doesn't already have the given role, for this function resets abilities like how many amulets the amulet holder has.
def swap(rolename,name,id,channel,uses,votes,threatened,enchanted,demonized,powdered,frozen,undead,lovers,zombies,sleepers,souls,amulets):
    if rolename == "Innocent":
        return role.Innocent(name,id,channel,0,votes,threatened,enchanted,demonized,powdered,frozen,undead,lovers,zombies,sleepers,souls,amulets)
    if rolename == "Alcoholic":
        return role.Alcoholic(name,id,channel,0,votes,threatened,enchanted,demonized,powdered,frozen,undead,lovers,zombies,sleepers,souls,amulets)
    if rolename == "Amulet Holder":
        return role.Amulet_Holder(name,id,channel,1,votes,threatened,enchanted,demonized,powdered,frozen,undead,lovers,zombies,sleepers,souls,amulets.append(id))
    if rolename == "Assassin":
        return role.Assassin(name,id,channel,0,votes,threatened,enchanted,demonized,powdered,frozen,undead,lovers,zombies,sleepers,souls,amulets)
    

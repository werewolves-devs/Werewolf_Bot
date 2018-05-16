import roles as role

# This function changes a player's role to a given role.
# Make sure the player doesn't already have the given role, for this function resets abilities like how many amulets the amulet holder has.
def swap(rolename,id,channel,uses,votes,threatened,enchanted,demonized,powdered,frozen,undead,bites,bitten,lovers,zombies,sleepers,souls,amulets):
    # List of people that can kill most players
    std_killers = ["Innocent", "Assassin", "Barber", "Cult Leader", "Executioner", "Huntress", "Witch", "Werewolf", "Lone Wolf", "Devil", "Wager", "Horseman", "Pyromancer"]
    
    if rolename == "Innocent":
        return role.Innocent("Innocent",id,channel,std_killers,0,votes,threatened,enchanted,demonized,powdered,frozen,undead,bites,bitten,lovers,zombies,sleepers,souls,amulets)
    if rolename == "Alcoholic":
        return role.Alcoholic("Alcoholic",id,channel,std_killers,0,votes,threatened,enchanted,demonized,powdered,frozen,undead,bites,bitten,lovers,zombies,sleepers,souls,amulets)
    if rolename == "Amulet Holder":
        return role.Amulet_Holder("Amulet Holder",id,channel,std_killers,1,votes,threatened,enchanted,demonized,powdered,frozen,undead,bites,bitten,lovers,zombies,sleepers,souls,amulets.append(id))
    if rolename == "Assassin":
        return role.Assassin("Assassin",id,channel,std_killers,0,votes,threatened,enchanted,demonized,powdered,frozen,undead,bites,bitten,lovers,zombies,sleepers,souls,amulets)

# Function that recognizes input of the user and translate it to what role it may refer to.
# It returns the correct name of the role
def role_interpret(user_msg):
    # TODO
    return "Spectator"
    

    
# For testing purposes. This will not execute if this file is imported by another file.
if __name__ == "__main__":
    print role.Spectator("1","000000000")
    rolerino = swap("Innocent","0","123456789",0,1,0,False,False,False,False,False,0,False,["Buddy1913","HurricanKai"],[],["FriedPotatoe"],-1,[])
    print rolerino

import roles as role

# This function changes a player's role to a given role.
# Make sure the player doesn't already have the given role, for this function resets abilities like how many amulets the amulet holder has.
def swap(rolename):
    # TODO
    return True

# Function that recognizes input of the user and translate it to what role it may refer to.
# It returns the correct name of the role
def role_interpret(user_msg):
    # TODO
    return "Spectator"
    

    
# For testing purposes. This will not execute if this file is imported by another file.
if __name__ == "__main__":
    print(role.Spectator("1","000000000"))
    rolerino = swap("Innocent","0","123456789",0,1,0,False,False,False,False,False,0,False,["Buddy1913","HurricanKai"],[],["FriedPotatoe"],-1,[])
    print(rolerino)

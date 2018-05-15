# Checks if a file can be converted into an integer.
# If it cannot, the function returns false.
def check_for_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Checks if a user has a specified role
# Returns True if they have the given role, False if they don't
def is_auth(member,role):
    
    # TODO
    # Claimed by NONE
    
    return False

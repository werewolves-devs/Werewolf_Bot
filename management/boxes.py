import random

# In this file, the Python program interacts with the box API

def create_hash(length=24):
    hash_table = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    , '-', '_', '!', '#', '(', ')', '*', '<', '>', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    
    hash_found = False
    attempts = 0

    while not hash_found:
        if attempts > 10000:
            print('This is very unlikely, but it seems too many tokens have been created!')
            print('Please try a higher number for the hash the length.')
            return False

        hash_value = ''
        for i in range(length):
            hash_value += random.choice(hash_table)
        
        # Make sure the value hasn't been produced before
        # (Even though the odds are minimal)
        if True:
            pass
            hash_found = True
        attempts += 1

    # Insert the given token into the API
    pass #TODO

    # Save the database
    pass #TODO

    return True
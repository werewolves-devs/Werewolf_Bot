from config import prefix
from emoji import UNICODE_EMOJI
from management.db import emoji_to_player
from management.position import roles_list

# Makes sure the message has at least the needed amount of users.
# If the message contains emojis, they should be converted to ids as well. Mentions have priority, however.
# The command should return the given amount of user ids, or, if equal to -1, should return them all.
def users(message,amount = -1, delete_duplicates = True):
    user_table = [person.id for person in message.mentions]

    for argument in message.content.split(' '):
        response = emoji_to_player(argument)

        if response != None:
            user_table.append(response)
    
    if delete_duplicates == True:
        user_table = list(set(user_table))
    
    if max(amount,1) > len(user_table):
        return False

    if amount == -1:
        return user_table
    
    return [user_table[i] for i in range(amount)]


# Makes sure the message has at least the needed amount of integers.
# The command should return the given amount of numbers, or, if equal to -1, should return them all.
def numbers(message,amount = -1, delete_duplicates = False):
    number_table = []

    for argument in message.content.split(' '):
        if check_for_int(argument):
            number_table.append(int(argument))
    
    if delete_duplicates == True:
        number_table = list(set(number_table))
    
    if max(amount,1) > len(number_table):
        return False
    
    if amount == -1:
        return number_table
    
    return [number_table[i] for i in range(amount)]

# Makes sure the message has at least the needed amount of emojis.
# The command should return the given amount of numbers, or, if equal to -1, should return them all.
def emojis(message,amount = -1, delete_duplicates = True):
    emoji_table = []

    for argument in message.content.split(' '):
        if argument in UNICODE_EMOJI:
            emoji_table.append(argument)
    
    if delete_duplicates == True:
        emoji_table = list(set(emoji_table))
    
    if max(amount,1) > len(emoji_table):
        return False
    
    if amount == -1:
        return emoji_table
    
    return [emoji_table[i] for i in range(amount)]

# Makes sure the message has at least the needed amount of roles.
# The command should return the given amount of numbers, or, if equal to -1, should return them all.
def roles(message,amount= -1,delete_duplicates = False):
    role_table = []

    for argument in message.content.split(' '):
        if argument in roles_list:
            role_table.append(argument)
    
    if delete_duplicates == True:
        role_table = list(set(role_table))
    
    if max(amount,1) > len(role_table):
        return False
    
    if amount == -1:
        return role_table
    
    return [role_table[i] for i in range(amount)]

# Checks if a file can be converted into an integer.
# If it cannot, the function returns false.
def check_for_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Checks if an input requests a given command
def is_command(message,commandlist,help=False):
    for command in commandlist:
        if message.content.startswith(prefix + command) and help == False:
            return True
        if message.content.startswith(prefix + 'help ' + command) and help == True:
            return True
    return False

if __name__ == "__main__":
    class message:
        content = "Deze tekst is Nederlands, maar bevat 4 cijfers; 1999 8 en 1 ! Jazeker, dat zijn er vier."
    
    x = message()
    print numbers(x)
    print numbers(x,3)
    print numbers(x,5)

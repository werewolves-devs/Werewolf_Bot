import db

# Checks if a file can be converted into an integer.
# If it cannot, the function returns false.
def check_for_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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
    
    raise ValueError("Unable to convert \'{}\' to SQLite position.".format(column))

# Makes sure the message has at least the needed amount of users.
# If the message contains emojis, they should be converted to ids as well. Mentions have priority, however.
# The command should return the given amount of user ids, or, if equal to -1, should return them all.
def users(message,amount = -1, delete_duplicates = True):
    user_table = [person.id for person in message.mentions]

    for argument in message.content.split(' '):
        response = db.emoji_to_player(argument)

        if response != None:
            user_table.append(response)
    
    if delete_duplicates == True:
        user_table = list(set(user_table))
    
    if amount > len(user_table):
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
    
    if amount > len(number_table):
        return False
    
    if amount == -1:
        return number_table
    
    return [number_table[i] for i in range(amount)]

if __name__ == "__main__":
    class message:
        content = "Deze tekst is Nederlands, maar bevat 4 cijfers; 1999 8 en 1 ! Jazeker, dat zijn er vier."
    
    x = message()
    print numbers(x)
    print numbers(x,3)
    print numbers(x,5)
    print ''


    print positionof("demonized")
    print positionof("bites")
    print positionof("id")
    print positionof("Something that doesn't exist! :D")

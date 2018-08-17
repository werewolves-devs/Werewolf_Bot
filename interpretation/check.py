import config
from emoji import UNICODE_EMOJI
from management.db import emoji_to_player, isParticipant
from management.position import roles_list

# Makes sure the message has at least the needed amount of users.
# If the message contains emojis, they should be converted to ids as well. Mentions have priority, however.
# The command should return the given amount of user ids, or, if equal to -1, should return them all.
def users(message,amount = -1, delete_duplicates = True, must_be_participant = False):
    """Return the requested amount of user ids in a list. If the amount is -1, all users are given.

    Keyword arguments:
    message -> the Discord message to inspect
    amount -> the wanted amount of users in a list
    delete_duplicates -> filter out users that are mentioned twice in the message
    """
    user_table = [person.id for person in message.mentions]

    if must_be_participant == True:
        for user in user_table:
            if not isParticipant(user):
                user_table.remove(user)

    for argument in message.content.split(' '):
        response = emoji_to_player(argument)

        if response != None:
            user_table.append(int(response))

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
    """Return the requested amount of integers in a list from the given message. If the amount is -1, all users are given.
    If there are not enough integers, or no integers at all, the function returns False.

    Keyword arguments:
    message -> the Discord message to inspect
    amount -> the wanted amount of integers in the list
    delete_duplicates -> filter out integers that are mentioned twice in the message
    """
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
    """Return the requested amount of (vanilla) emojis in a list from a message. If the amount is -1, all emojis are given.
    If there are not enough emojis or none at all, the function returns False.

    Keyword arguments:
    message -> the Discord message to inspect
    amount -> the wanted amount of integers in the list
    delete_duplicates -> filter out emojis that are mentioned twice in the message
    """

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
    """Return the requested amount of roles that are mentioned in the message as a list. If the amount is -1, all roles are given.
    If there are not enough roles or none at all, the function returns False.

    Keyword arguments:
    message -> the Discord message to inspect
    amount -> the wanted amount of integers in the list
    delete_duplicates -> filter out roles that are mentioned twice in the message
    """

    role_table = []

    for i in range(len(message.content)):
        for role in roles_list:
            if message.content[i:].lower().startswith(role.lower()):
                role_table.append(role)

    # Remove overlapping role names
    for role in role_table:
        if role == 'White Werewolf':
            role_table.remove('Werewolf')
        if role == 'Priestess':
            role_table.remove('Priest')

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
    """Returns True if the value s is or can be converted to an integer. Returns False otherwise."""
    try:
        int(s)
        return True
    except ValueError:
        return False

# Checks if an input requests a given command
def is_command(message,commandlist,help=False,prefix=config.ww_prefix):
    """Check if the message starts with the given command or its aliases.

    Keyword arguments:
    message -> the Discord message
    commandlist -> list of possible commands that return True if the prefix is put in front of them
    help -> when set to True, return True when the message starts with the prefix, then help, and then the command.
    """
    for command in commandlist:
        if message.content.startswith(prefix + command) and help == False:
            return True
        if message.content.startswith(prefix + 'help ' + command) and help == True:
            return True
        if message.content.startswith('?' + command) and help == True:
            return True
    return False

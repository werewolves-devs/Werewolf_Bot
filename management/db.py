import sqlite3
from config import database, max_channels_per_category
from management.position import positionof, check_for_int

conn = sqlite3.connect(database)
c = conn.cursor()

def execute(cmd_string):
    """Execute a command straight into the database. Avoiding usage recommended.

    Keyword arguments:
    cmd_string -> the command to be executed upon the database
    """

    c.execute(cmd_string)

    conn.commit()

    return c.fetchall()

def poll_list():
    """Return a list of users to be added to the poll.
    The first argument is the user's id, the second is their emoji, and the third and fourth are arguments that no longer\
    allow the user to vote on them."""

    c.execute("SELECT id, emoji, frozen, abducted FROM game")

    return c.fetchall()

def player_list():
    """Return a list of users that are signed up in the database. Dead players and spectators are returned as well."""
    return [item[0] for item in poll_list()]

# This function takes an argument and looks up if there's a user with a matching emoji.
# If found multiple, which it shouldn't, it takes the first result and ignores the rest.
def emoji_to_player(emoji):
    """Look up the user's id that corresponds with the given emoji. Returns None if the user doesn't exist, \
    and returns the user's id if present.

    Keyword arguments:
    emoji -> given emoji
    """

    c.execute("SELECT id FROM game WHERE emoji =?", (emoji,))

    try:
        return c.fetchall()[0][0]
    except TypeError:
        return None
    except IndexError:
        return None
    else:
        return None

# Get all of a user's data from the database
def get_user(id):
    """Gather all of a user's data from the database.

    Keyword arguments:
    id -> the user's id
    """

    c.execute("SELECT * FROM game WHERE id=?", (id,))

    try:
        return c.fetchone()
    except TypeError:
        return None
    except IndexError:
        return None
    else:
        return None

# This function makes sure the user is a participant.
# If the user is a spectator, it returns whatever spectator is set to.
def isParticipant(id,spectator = False,dead = False):
    """Checks if the user is a registered participant in the database

    Keyword arguments:
    id -> the user's id
    spectator -> value the function should return if the user is a spectator
    dead -> value the function should return if the user is dead
    """

    if get_user(id) in [None, []]:
        return False

    if db_get(id,"role") == u'Spectator':
        return spectator

    if db_get(id,'role') == u'Dead':
        return dead

    return True

# This function returns a user's personal channel.
def personal_channel(user_id,channel_id):
    """Returns True if the given channel is the user's personal channel.

    Keyword arguments:
    user_id -> the user's id
    channel_id -> the channel's id
    """
    if db_get(user_id,"channel") == str(channel_id):
        return True
    return False

# Gather a user's bit of information from the database.
def db_get(user_id,column):
    """Gain a specific bit of information from a given player

    Keyword arguments:
    user_id -> the user's id
    column -> the relevant part of info
    """
    values = get_user(user_id)
    if values == None:
        return None
    return values[positionof(column)]

# Change a user's bit of information in the database.
def db_set(user_id,column,value):
    """Alter a specific bit of information of a given player

    Keyword argumentsL
    user_id -> the user's id
    column -> the relevant part of info
    value -> the new value it should be set to
    """
    c.execute("UPDATE game SET {}=? WHERE id=?".format(column), (value,user_id))
    conn.commit()

# Add a kill to the kill queue.
# Apply in case of an end-effect kill.
def add_kill(victim_id,role,murderer = ""):
    """Add a new order to the kill queue.

    Keyword arguments:
    victim_id -> the id of the victim to be attacked
    role -> the role of the attacker
    murderer -> id of the attacker (random attacker if multiple)
    """
    data = [victim_id,role,murderer]
    c.execute("INSERT INTO 'death-row' ('id','victim','role','murderer') VALUES (NULL,?,?,?)",data)
    conn.commit()
    return

# Gather a kill from the kill queue. Pay attention; the function auto-deletes the kill from the list
def get_kill():
    """Receive a kill from the kill queue. Receiving the file also deletes the order from the database."""
    c.execute("SELECT * FROM 'death-row'")

    try:
        order = c.fetchone()

        if order == None:
            return None
    except TypeError:
        return None
    except IndexError:
        return None

    kill = [order[i] for i in range(4)]
    c.execute("DELETE FROM 'death-row' WHERE (id =?)",(kill[0],))
    conn.commit()
    return kill

# Register a new channel to the database
def add_channel(channel_id,owner):

    """Add a channel to the database.

    Keyword arguments:
    channel_id -> the channel's id
    owner -> the owner's id
    """
    c.execute("SELECT * FROM categories")

    # Tell the categories database the given category has yet received another channel
    c.execute("UPDATE categories SET channels = channels + 1 WHERE current = 1")

    c.execute("INSERT INTO 'channels' ('channel_id','owner') VALUES (?,?)",(channel_id,owner))
    conn.commit()

# Change a user's value in a specific channel
def set_user_in_channel(channel_id,user_id,number):

    """Set a specific user's value in a given channel.
    0 - no access
    1 - access
    2 - frozen
    3 - abducted
    4 - dead

    Keyword arguments:
    channel_id -> the channel's id
    user_id -> the user's id
    number -> the value to set
    """
    data = [number,channel_id]
    c.execute("UPDATE \"channels\" SET \"id{}\"=? WHERE \"channel_id\" =?".format(user_id),data)
    conn.commit()

# This function visits every channel where the user has value "old" and sets it to value "new"
# It then returns all channels that it has changed.
def channel_change_all(user_id,old,new):
    """Change all values from one to another for a given user. Returns a list of altered channels.

    Keyword arguments:
    user_id -> the user's id
    old -> the old value to change
    new -> the new value to change to
    """
    c.execute("SELECT channel_id FROM 'channels' WHERE id{} =?".format(user_id),(old,))
    change_list = c.fetchall()
    data = [new,old]
    c.execute("UPDATE 'channels' SET 'id{0}'=? WHERE id{0} =?".format(user_id),data)

    conn.commit()

    return [element[0] for element in change_list]

# Gain all information of a channel
# If the channel does not exist, it returns None
# When given a specific user_id or the argument owner, it returns that specific bit of data
def channel_get(channel_id,user_id = ''):
    """Gain the information of a channel. Returns None if the channel doesn't exist, or if the user isn't found.

    Keyword arguments:
    channel_id -> the channel's id
    user_id -> (optional) the specific value. Returns all info if blank and returns the owner's id when set to 'owner'
    """

    if user_id == '':
        c.execute("SELECT * FROM 'channels' WHERE channel_id =?",(channel_id,))
    elif user_id == 'owner':
        c.execute("SELECT owner FROM 'channels' WHERE channel_id =?",(channel_id,))
        try:
            return c.fetchone()[0]
        except ValueError:
            return None
        else:
            return None
    else:
        c.execute("SELECT * FROM channel_rows WHERE id =?",(user_id,))
        if c.fetchone() == None:
            return None

        column = 'id' + str(user_id)
        c.execute("SELECT {} FROM 'channels' WHERE channel_id =?".format(column),(channel_id,))
    return c.fetchone()

def get_columns():
    """Gain all data about ALL channels. Usage not recommended."""
    c.execute("SELECT * FROM channel_rows")
    return c.fetchall()

def abduct(user_id):
    """Returns a list of channels that need to be changed to abduct a player

    Keyword arguments:
    user_id -> the user's id
    """
    return channel_change_all(user_id,1,3)

def unabduct(user_id):
    """Returns a list of channels that need to be changed to unabduct a player

    Keyword arguments:
    user_id -> the user's id
    """
    return channel_change_all(user_id,3,1)

def freeze(user_id):
    """Returns a list of channels that need to be changed to freeze a player

    Keyword arguments:
    user_id -> the user's id
    """
    return channel_change_all(user_id,1,2)

def unfreeze(user_id):
    """Returns a list of channels that need to be changed to unfreeze a player

    Keyword arguments:
    user_id -> the user's id
    """
    return channel_change_all(user_id,2,1)

def kill(user_id):
    """Returns a list of channels that need to be changed to kill a player

    Keyword arguments:
    user_id -> the user's id
    """
    return [channel_change_all(user_id,i,4) for i in range(4)]

def get_category():
    """Receives the category that the current cc should be created in. If it cannot find a category,
    or if the category is full, it will return None with the intention that a new category is created in main.py"""
    c.execute("SELECT * FROM categories WHERE current = 1")
    category = c.fetchone()

    if category == None:
        return None
    if category[2] >= max_channels_per_category:
        return None

    return int(category[1])

def add_category(id):
    """Let the datbase know a new category has been appointed for the cc's, which has the given id.

    Keyword arguments:
    id -> the id of the category"""
    c.execute("UPDATE categories SET current = 0;")
    c.execute("INSERT INTO categories ('id') VALUES (?);",(id,))
    conn.commit()

def is_owner(user_id,channel_id):
    """This function returns True is the given user is the owner of a given cc.
    Returns False if the user is not the owner, if the user doesn't exist or if the channel isn't found.

    Keyword arguments:
    id -> the id of the user
    channel -> the id of the channel"""

    # Check if the user exists
    c.execute("SELECT * FROM channel_rows WHERE id =?",(user_id,))
    if c.fetchone() == None or check_for_int(user_id) == False or check_for_int(channel_id):
        return False

    owner = channel_get(channel_id,'owner')
    if int(owner) == int(user_id):
        return True

    return False

def count_categories():
    """This function counts how many categories are currently registered, and returns the value as an integer."""
    c.execute("SELECT COUNT(*) FROM 'categories';")
    return c.fetchone()[0]

# Add a new participant to the database
def signup(user_id,name,emoji):
    c.execute("INSERT INTO game (id,name,emoji,channel,role,fakerole,lovers,sleepers,amulets,zombies) VALUES (?,?,?,'#gamelog','Spectator','Spectator','','','','')", (user_id,name,emoji))
    c.execute("ALTER TABLE channels ADD COLUMN 'id{}' TEXT NOT NULL DEFAULT 0".format(user_id))
    c.execute("INSERT INTO channel_rows ('id') VALUES (?)",(user_id,))
    conn.commit()

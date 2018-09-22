import sqlite3
import random
from config import database, max_channels_per_category, max_participants
from management.position import positionof, check_for_int, wolf_pack

conn = sqlite3.connect(database)
c = conn.cursor()

class PollToEvaluate:
    def __init__(self,database_tuple):
        self.purpose = database_tuple[1]
        self.blamed = database_tuple[2]
        self.channel = database_tuple[3]

        self.msg_table = [int(database_tuple[i+4]) for i in range(len(database_tuple) - 4) if int(database_tuple[i+4]) != 0]

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

def player_list(alive_only = False,available_only = False):
    """Return a list of users that are signed up in the database. Dead players and spectators are returned as well."""
    player_list = [int(item[0]) for item in poll_list()]
    
    if alive_only == False and available_only == False:
        return player_list

    if available_only == False:
        player_list = [player for player in player_list if db_get(player,'role') not in ['Spectator','Dead']]

    return [player for player in player_list if int(db_get(player,'abducted')) == 0 and int(db_get(player,'frozen')) == 0]

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
    conn.commit()

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
def isParticipant(id,spectator = False,dead = False,suspended = False):
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

    if db_get(id,'role') == u'Suspended':
        return suspended

    return True

# This function returns a user's personal channel.
def personal_channel(user_id,channel_id):
    """Returns True if the given channel is the user's personal channel.

    Keyword arguments:
    user_id -> the user's id
    channel_id -> the channel's id
    """
    if int(db_get(user_id,"channel")) == int(channel_id):
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
    positionof(column) # Make sure the value is valid.
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
def add_channel(channel_id,owner,secret=False):

    """Add a channel to the database.

    Keyword arguments:
    channel_id -> the channel's id
    owner -> the owner's id
    """
    c.execute("SELECT * FROM categories")

    # Tell the categories database the given category has yet received another channel
    if not secret:
        c.execute("UPDATE categories SET channels = channels + 1 WHERE current = 1")
    else:
        c.execute("UPDATE 'secret_categories' SET channels = channels + 1 WHERE current = 1")

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

    return [int(element[0]) for element in change_list]

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
        except TypeError:
            return None
        else:
            return None
    else:
        c.execute("SELECT * FROM channel_rows WHERE id =?",(user_id,))
        if c.fetchone() == None:
            return None

        column = 'id' + str(user_id)
        c.execute("SELECT {} FROM 'channels' WHERE channel_id =?".format(column),(channel_id,))
        return c.fetchone()[0]
    return c.fetchone()

def get_columns():
    """Gain all data about ALL channels. Usage not recommended."""
    c.execute("SELECT * FROM channel_rows")
    return c.fetchall()

def get_category(secret = False):
    """Receives the category that the current cc should be created in. If it cannot find a category,
    or if the category is full, it will return None with the intention that a new category is created in main.py"""

    # Keep in mind; secret channels and conspiracy channels use different categories.
    if not secret:
        c.execute("SELECT * FROM categories WHERE current = 1")
    else:
        c.execute("SELECT * FROM 'secret_categories' WHERE current = 1")

    category = c.fetchone()

    if category == None:
        return None
    if category[2] >= max_channels_per_category:
        return None

    return int(category[1])

def add_category(id,secret=False):
    """Let the datbase know a new category has been appointed for the cc's, which has the given id.

    Keyword arguments:
    id -> the id of the category"""
    if not secret:
        c.execute("UPDATE categories SET current = 0;")
        c.execute("INSERT INTO categories ('id') VALUES (?);",(id,))
    else:
        c.execute("UPDATE 'secret_categories' SET current = 0;")
        c.execute("INSERT INTO 'secret_categories' ('id') VALUES (?);",(id,))

    conn.commit()

def is_owner(user_id,channel_id):
    """This function returns True is the given user is the owner of a given cc.
    Returns False if the user is not the owner, if the user doesn't exist or if the channel isn't found.

    Keyword arguments:
    user_id -> the id of the user
    channel_id -> the id of the channel"""

    # Check if the user exists
    c.execute("SELECT * FROM channel_rows WHERE id =?",(user_id,))
    if c.fetchone() == None or check_for_int(user_id) == False or check_for_int(channel_id) == False:
        print('Column doesn\'t exist!')
        return False

    owner = channel_get(channel_id,'owner')
    if owner == None:
        return False

    if int(owner) == int(user_id):
        return True

    return False

def count_categories(secret=False):
    """This function counts how many categories are currently registered, and returns the value as an integer."""
    if not secret:
        c.execute("SELECT COUNT(*) FROM 'categories';")
    else:
        c.execute("SELECT COUNT(*) FROM 'secret_categories';")
    return c.fetchone()[0]

def get_channel_members(channel_id, number = 1):
    """This function returns a list of user ids that have the given number in a given channel.
    If it finds none or if the channel wasn't found, the function returns an empty list.

    Keyword arguments:
    channel_id -> id of the channel
    number -> number that is to be selected"""
    c.execute("SELECT * FROM 'channel_rows'")
    members = []

    for user in c.fetchall():
        if channel_get(channel_id,int(user[0])) == None:
            print("Warning: The bot has attempted to look for a channel that does not exist!")
            return []
        if int(channel_get(channel_id,int(user[0]))) == int(number):
            members.append(int(user[0]))
    return members

def get_secret_channels(role):
    """Get a list of secret channels that have a certain role. The function returns a list of integers.  
    
    Keyword arguments:  
    role -> the role of which the channel was created"""

    c.execute("SELECT * FROM 'secret_channels' WHERE role =?",(role,))

    return [int(pointer[1]) for pointer in c.fetchall()]

def add_secret_channel(channel_id,role):
    """Add a pointer towards a new secret channel in the database. Note this only adds the pointer, not the actual channel.  
    
    Keyword arguments:  
    channel_id -> the id of the secret channel  
    role -> the role that owns the channel"""

    c.execute("INSERT INTO 'secret_channels' ('role','channel_id') VALUES (?,?);",(role,channel_id))
    conn.commit()

def amulets(user_id):
    """Display a list of amulets that the given user owns."""
    amulet_channels = []
    for channel_id in get_secret_channels('Amulet_Holder'):
        if int(channel_get(channel_id,user_id)) in [1,2,3]:
            amulet_channels.append(int(channel_id))
    return amulet_channels

def has_amulet(user_id):
    """Returns boolean whether the user has an amulet or not."""
    if amulets(user_id) != []:
        return True
    return False

def insert_deadie(user_id):
    """Add a new deadie to the list. This list will be evaluated for the storytime."""
    c.execute("SELECT * FROM 'deadies' WHERE user_id =?",(user_id,))
    if c.fetchall() == []:
        c.execute("INSERT INTO 'deadies' ('user_id') VALUES (?);",(user_id,))
    conn.commit()

def get_deadies():
    """Gain the list of deadies from the database."""
    c.execute("SELECT * FROM 'deadies'")
    return [int(buddy[0]) for buddy in c.fetchall()]

def delete_deadies():
    """Remove all deadies from the database."""
    c.execute("DELETE FROM 'deadies'")
    conn.commit()

# Add a new participant to the database
def signup(user_id,name,emoji):
    c.execute("INSERT INTO 'game'('id','name','emoji') VALUES (?,?,?);", (user_id,name,emoji))
    c.execute("SELECT * FROM channel_rows WHERE id =?",(user_id,))
    if c.fetchall() == []:
        c.execute("ALTER TABLE 'channels' ADD COLUMN 'id{}' TEXT NOT NULL DEFAULT 0".format(user_id))
        c.execute("INSERT INTO 'channel_rows' ('id') VALUES (?)",(user_id,))
    conn.commit()

def add_poll(msg_table,purpose,channel_id,user_id = 0):
    """Add a new poll to the database. The poll is saved so it can be evaluated later on.

    msg_table -> the list of messages that contain the poll
    purpose -> the reason the poll is made for. Examples are 'wolf', 'mayor', 'lynch' or 'cult'
    user_id -> the user who is \"responsible\" for the lynch. Leave blank if daily poll."""
    amount = int(max_participants/20)+1
    if msg_table == []:
        raise ValueError("Cannot insert empty poll into database.")
    if len(msg_table) > amount:
        raise IndexError("Poll needed more space in database than expected!")

    request_msg = "INSERT INTO 'polls'('purpose','user_id','channel'"
    request2_msg = ") VALUES ('{}','{}',{}".format(purpose,user_id,channel_id)

    for i in range(len(msg_table)):

        request_msg += ",'part{}'".format(i+1)
        request2_msg += ",{}".format(msg_table[i].id)

    query = request_msg + request2_msg + ");"
    c.execute(query)
    conn.commit()

def get_all_polls():
    """Gain the polls registered the database. As all polls are always evaluated simultaneously,
    the polls are deleted from the database. If they really need to be kept, they can always be saved again."""
    c.execute("SELECT * FROM 'polls'")
    answer_table = c.fetchall()
    c.execute("DELETE FROM 'polls'")
    conn.commit()

    return [PollToEvaluate(item) for item in answer_table]

def add_freezer(user_id,victim_id,role):
    """This function saves an ice king's guess in the database. If a guess about that player already exists,
    it is overwritten, and the old role is returned.

    user_id -> the role of the ice king casting the guess
    victim_id -> the player whose role is guessed
    role -> the role that victim_id is guessed to be  """
    c.execute("SELECT role FROM 'freezers' WHERE victim =? AND king =?",(victim_id,user_id))
    answer = c.fetchone()
    if answer == None:
        c.execute("INSERT INTO 'freezers' (king,victim,role) VALUES (?,?,?)",(user_id,victim_id,role))
        conn.commit()
        return None
    c.execute("UPDATE 'freezers' SET 'role' =? WHERE king =? AND victim =?",(role,user_id,victim_id))
    conn.commit()
    return answer[0]

def get_freezers(user_id):
    """Get a list of all the guesses an ice king has made so far, including their roles.

    user_id -> the id of the ice king"""
    c.execute("SELECT victim, role FROM freezers WHERE king =?",(user_id,))
    return c.fetchall()

def delete_freezer(user_id,victim_id):
    """Remove a guessed user from the database. If the user wasn\'t in the database, return False.
    Else, return True when removed successfully.

    user_id -> the player removing the guess
    victim_id -> the player being guessed"""
    c.execute("SELECT * FROM freezers WHERE king =? AND victim =?",(user_id,victim_id))
    if c.fetchone() == None:
        return False
    c.execute("DELETE FROM freezers WHERE king =? AND victim =?",(user_id,victim_id))
    conn.commit()
    return True

def add_standoff(victim_id,role,murderer):
    """Add a new order to the kill queue.

    Keyword arguments:
    victim_id -> the id of the victim to be attacked
    role -> the role of the attacker
    murderer -> id of the attacker (random attacker if multiple)
    """
    data = [victim_id,role,murderer]
    c.execute("INSERT INTO 'standoff' ('id','victim','role','murderer') VALUES (NULL,?,?,?)",data)
    conn.commit()
    return

def get_standoff(user_id):
    """Gain a list of standoffs from a user; this is a list of players they will take with them when they die."""
    c.execute("SELECT * FROM 'standoff' WHERE murderer =?",(user_id,))

    returntable = []
    for element in c.fetchall():
        returntable.append([element[i] for i in range(4)])

    return returntable

def delete_standoff(standoff_id):
    """Remove a standoff from the database. This is generally not needed, but is used for occasions like the huntress who chooses a new target.

    Keyword arguments:
    standoff_id -> the database id of the standoff"""
    c.execute("DELETE FROM 'standoff' WHERE id =?",(standoff_id,))
    conn.commit()

def delete_hookers():
    """Remove all hooker standoffs from the database."""
    c.execute("DELETE FROM 'standoff' WHERE role =='Hooker'")
    c.execute("UPDATE 'game' SET sleepingover =0")
    conn.commit()

def random_wolf():
    """Find and get a random wolf pack member"""
    wolfies = [user_id for user_id in player_list() if db_get(user_id,'role') in wolf_pack]
    if wolfies == []:
        print("This is strange! A random wolf is called, which shouldn't happen if there aren't any wolves around.")
        return ''
    return wolfies[random.randint(0,len(wolfies)-1)]

def random_cult():
    """Find and get a random cult leader/member"""
    culties = [user_id for user_id in player_list() if db_get(user_id,'role') in ['Cult Leader','Cult Member']]
    if culties == []:
        print('How is the random_cult() function called when there isn\'t a cult leader around? Strange!')
        return ''
    return culties[random.randint(0,len(culties)-1)]

def add_trash_channel(channel_id):
    """Add a new trash channel to the database."""
    c.execute("SELECT * FROM 'trashy' WHERE 'channel' =?;",(channel_id,))
    if c.fetchall() == []:
        c.execute("INSERT INTO 'trashy'('channel') VALUES (?);",(channel_id,))
        conn.commit()

def add_trash_message(message_id,channel_id):
    """Add a message to the trash bin. The function makes sure the channel's a trash channel.
    If it's not, then the message isn't stored in the database."""

    c.execute("SELECT * FROM 'trashy' WHERE 'channel' =?",(channel_id,))
    if c.fetchall() != []:
        c.execute("INSERT INTO 'trashcan'('message','channel') VALUES (?,?);",(message_id,channel_id))
        conn.commit()

def empty_trash_channel(channel_id):
    """Remove all messages stored from a given channel.  
    The function returns a list of message ids that were linked to the given channel id."""
    c.execute("SELECT * FROM 'trashcan' WHERE 'channel' =?;",(channel_id))
    message_table = [item[0] for item in c.fetchall()]

    c.execute("DELETE FROM 'trashcan' WHERE 'channel' =?",(channel_id,))
    conn.commit()

    return message_table


def add_listener(spy,innocent):
    """Add a new listener to the database. A listener is a bridge from one channel to another.
    This function allows roles like the flute player to keep contact with their victims."""
    c.execute("INSERT INTO 'listener'('innocent','spy') VALUES (?,?)",(innocent,spy))
    conn.commit()

def find_spies(innocent):
    """Find all channels that this message's content needs to be sent to."""
    c.execute("SELECT * FROM 'listener' WHERE innocent=?",(innocent,))
    return [listener[1] for listener in c.fetchall()]

def find_innocents(spy):
    """Find all channels this spy channel is spying on."""
    c.execute("SELECT * FROM 'listener' WHERE spy=?",(spy,))
    return [listener[0] for listener in c.fetchall()]

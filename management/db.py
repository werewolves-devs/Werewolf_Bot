import sqlite3
from config import database
from management.position import positionof

conn = sqlite3.connect(database)
c = conn.cursor()

def execute(cmd_string):
    c.execute(cmd_string)

    conn.commit()

    return c.fetchall()

def poll_list():
    c.execute("SELECT id, emoji, frozen FROM game")

    return c.fetchall()

# This function takes an argument and looks up if there's a user with a matching emoji.
# If found multiple, which it shouldn't, it takes the first result and ignores the rest.
def emoji_to_player(emoji):
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
def isParticipant(id,spectator = False):
    if get_user(id) in [None, []]:
        return False
    
    if db_get(id,"role") == u'Spectator':
        return spectator

    return True

# This function returns a user's personal channel.
def personal_channel(user_id,channel_id):
    if db_get(user_id,"channel") == str(channel_id):
        return True
    
    return False

# Gather a user's bit of information from the database.
def db_get(user_id,column):
    return get_user(user_id)[positionof(column)]

# Change a user's bit of information in the database.
def db_set(user_id,column,value):
    c.execute("UPDATE game SET {}=? WHERE id=?".format(column), (value,user_id))
    conn.commit()

# Add a kill to the kill queue.
# Apply in case of an end-effect kill.
def add_kill(victim_id,role,murderer = ""):
    data = [victim_id,role,murderer]
    c.execute("INSERT INTO 'death-row' ('id','victim','role','murderer') VALUES (NULL,?,?,?)",data)    
    conn.commit()
    return

# Gather a kill from the kill queue. Pay attention; the function auto-deletes the kill from the list
def get_kill():
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
    c.execute("INSERT INTO 'channels' ('channel_id','owner') VALUES (?,?)",(channel_id,owner))
    conn.commit()

# Change a user's value in a specific channel
def set_user_in_channel(channel_id,user_id,number):
    # 0 - no access
    # 1 - access
    # 2 - frozen
    # 3 - abducted
    # 4 - dead
    data = [number,channel_id]
    c.execute("UPDATE \"channels\" SET \"id{}\"=? WHERE \"channel_id\" =?".format(user_id),data)
    conn.commit()

# This function visits every channel where the user has value "old" and sets it to value "new"
# It then returns all channels that it has changed.
def channel_change_all(user_id,old,new):
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
    if user_id == '':
        c.execute("SELECT * FROM 'channels' WHERE channel_id =?",(channel_id,))
    elif user_id == 'owner':
        c.execute("SELECT owner FROM 'channels' WHERE channel_id =?",(channel_id,))
        try:
            return c.fetchone()[1]
        except ValueError:
            return None
        else:
            return None
    else:
        column = 'id' + str(user_id)
        c.execute("SELECT {} FROM 'channels' WHERE channel_id =?".format(column),(channel_id,))
    return c.fetchone()

def get_columns():
    c.execute("SELECT * FROM channel_rows")
    return c.fetchall()

def abduct(user_id):
    return channel_change_all(user_id,1,3)

def unabduct(user_id):
    return channel_change_all(user_id,3,1)

def freeze(user_id):
    return channel_change_all(user_id,1,2)

def unfreeze(user_id):
    return channel_change_all(user_id,2,1)

def kill(user_id):
    return [channel_change_all(user_id,i,4) for i in range(4)]

# Add a new participant to the database
def signup(user_id,name,emoji):
    c.execute("INSERT INTO game (id,name,emoji,channel,role,fakerole,lovers,sleepers,amulets,zombies) VALUES (?,?,?,'#gamelog','Spectator','Spectator','','','','')", (user_id,name,emoji))
    c.execute("ALTER TABLE channels ADD COLUMN 'id{}' TEXT NOT NULL DEFAULT 0".format(user_id))
    c.execute("INSERT INTO channel_rows ('id') VALUES (?)",(user_id,))
    conn.commit()

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

# Get a user from the database
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

def isParticipant(id,spectator = False):
    if get_user(id) in [None, []]:
        return False

    if spectator == False and db_get(id,"role") == u'Spectator':
        return False

    return True

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

# Add a channel to the database
def new_channel(channel_id):


# Add a new participant to the database
def signup(user_id,name,emoji):
    c.execute("INSERT INTO game (id,name,emoji,channel,role,fakerole,lovers,sleepers,amulets,zombies) VALUES (?,?,?,'#gamelog','Spectator','Spectator','','','','')", (user_id,name,emoji))
    conn.commit()

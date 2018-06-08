import sqlite3
from config import database
from management.cmd_requirements import positionof

conn = sqlite3.connect(database)
c = conn.cursor()

def execute(cmd_string):
    c.execute(cmd_string)

    conn.commit()

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

# Gather a user's bit of information from the database.
def db_get(user_id,column):
    return get_user(user_id)[positionof(column)]

# Change a user's bit of information in the database.
def db_set(user_id,column,value):
    c.execute("UPDATE game SET ?=? WHERE id=?", (column,value,user_id))
    conn.commit()


def db_test():
    print c.execute("INSERT INTO game (id,name,emoji,channel,role,fakerole,lovers,sleepers,amulets,zombies) VALUES ('1','Randium003',':smirk:','#gamelog','Spectator','Spectator','','','','')")
    print get_user(1)
    print db_get(1,'channel')
    # These changes aren't saved, making them safe to test.
    return db_get(1,'name')

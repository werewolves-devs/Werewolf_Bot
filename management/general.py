import sqlite3
import config

conn = sqlite3.connect(config.general_database)
c = conn.cursor()

# Gather a user's bit of information from the database.
def gen_get(user_id,column):
    """Gain a specific bit of information from a given player.  

    Keyword arguments:  
    user_id -> the user's id  
    column -> the relevant part of info  
    """
    c.execute("SELECT {} FROM users WHERE id=?".format(column),(user_id,))
    value = c.fetchone()
    if value == None:
        return None
    return value[0]

# Change a user's bit of information in the database.
def gen_set(user_id,column,value):
    """Alter a specific bit of information of a given player

    Keyword arguments:
    user_id -> the user's id
    column -> the relevant part of info
    value -> the new value it should be set to
    """
    c.execute("UPDATE users SET {}=? WHERE id=?".format(column), (value,user_id))
    conn.commit()
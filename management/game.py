import sqlite3
import config

conn = sqlite3.connect(config.database)
c = conn.cursor()

# Gather a user's bit of information from the database.
def db_get(user_id,column):
    """Gain a specific bit of information from a given participant.  

    Keyword arguments:  
    user_id -> the user's id  
    column -> the relevant part of info  
    """
    c.execute("SELECT {} FROM gane WHERE id=?",(user_id,))
    value = c.fetchone
    if value == None:
        return None
    return value[0]

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
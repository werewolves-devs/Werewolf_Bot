import sqlite3
import config
import random

conn = sqlite3.connect(config.general_database)
c = conn.cursor()

def add_token(token,user_id):
    """Add a new token to the database.  
      
    Keyword arguments:  
    token -> the given token  
    user_id -> the user to whom the lootbox belongs"""

    c.execute("SELECT * FROM 'tokens' WHERE 'token' =?",(token,))
    if c.fetchall() != None:
        return False
    
    c.execute("INSERT INTO 'tokens' ('token','owner') VALUES ('?',?)",(token,user_id))
    conn.commit()
    return True
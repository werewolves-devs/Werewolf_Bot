import sqlite3
import config
import random


def add_token(token,user_id):
    """Add a new token to the database.  
      
    Keyword arguments:  
    token -> the given token  
    user_id -> the user to whom the lootbox belongs"""

    conn = sqlite3.connect(config.general_database)
    c = conn.cursor()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    if c.fetchone() != None:
        return None
    
    c.execute("INSERT INTO 'tokens' ('token','owner') VALUES (?,?)",(token,user_id))
    conn.commit()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    return c.fetchone()

def add_source1(token,source):
    """Register source 1 and add it to the token. Triggered when opening the box.  
    
    Keyword arguments:  
    token -> the opt's token"""

    conn = sqlite3.connect(config.general_database)
    c = conn.cursor()

    c.execute("UPDATE 'tokens' SET source1 =? WHERE token =?",(source,token))
    conn.commit()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    return c.fetchone()

def add_source2(token,source):
    """Register source 2 and add it to the token. Triggered when picking a choice.  
    
    Keyword arguments:  
    token -> the opt's token"""

    conn = sqlite3.connect(config.general_database)
    c = conn.cursor()

    c.execute("UPDATE 'tokens' SET source2 =? WHERE token =?",(source,token))
    conn.commit()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    return c.fetchone()

def add_options(token,choice1,choice2,choice3):
    """Register the three options into the database.  

    Keyword arguments:  
    token -> the options' token  
    choice1 -> option 1  
    choice2 -> option 2  
    choice3 -> option 3"""

    conn = sqlite3.connect(config.general_database)
    c = conn.cursor()

    c.execute("UPDATE 'tokens' SET opt1 =? WHERE token =?",(choice1,token))
    c.execute("UPDATE 'tokens' SET opt2 =? WHERE token =?",(choice2,token))
    c.execute("UPDATE 'tokens' SET opt3 =? WHERE token =?",(choice3,token))
    c.execute("UPDATE 'tokens' SET status =1 WHERE token =?",(token,))
    conn.commit()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    return c.fetchone()

def add_choice(token,choice):
    """Register the chosen option into the database.  
    
    Keyword arguments:  
    token -> the choice's token  
    choice -> the made choice"""

    conn = sqlite3.connect(config.general_database)
    c = conn.cursor()

    c.execute("UPDATE 'tokens' SET choice =? WHERE token =?",(choice,token))
    c.execute("UPDATE 'tokens' SET status =2 WHERE token =?",(token,))
    c.execute("UPDATE 'tokens' SET redeemed =DateTime('now') WHERE token =?",(token,))
    conn.commit()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    return c.fetchone()

def get_token_data(token):
    """Gain the info about a specific token  
    
    Keyword arguments:  
    token -> the token"""

    conn = sqlite3.connect(config.general_database)
    c = conn.cursor()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    return c.fetchone()

def token_status(token):
    """Validate if a token's real, and if it is, learn about its current status.  
    
    Status meanings:  
    -1 -> invalid (non-existent) token  
    0 -> token exists, unopened box  
    1 -> token exists, box opened but choice not picked yet  
    2 -> invalid token (already redeemed)"""

    conn = sqlite3.connect(config.general_database)
    c = conn.cursor()

    c.execute("SELECT * FROM 'tokens' WHERE token =?",(token,))
    result = c.fetchone()

    if result == None:
        return -1
    return result[2]
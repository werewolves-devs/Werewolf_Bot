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

def add_source1(token,source):
    """Register source 1 and add it to the token.  
    
    Keyword arguments:  
    token -> the opt's token"""
    c.execute("UPDATE 'tokens' SET 'source1' =? WHERE 'token' =?",(source,token))
    conn.commit()
    
def add_source2(token,source):
    """Register source 2 and add it to the token.  
    
    Keyword arguments:  
    token -> the opt's token"""
    c.execute("UPDATE 'tokens' SET 'source2' =? WHERE 'token' =?",(source,token))
    conn.commit()

def add_options(token,choice1,choice2,choice3):
    """Register the three options into the database.  

    Keyword arguments:  
    token -> the options' token  
    choice1 -> option 1  
    choice2 -> option 2  
    choice3 -> option 3"""
    c.execute("UPDATE 'tokens' SET 'opt1' =? WHERE 'token' =?",(choice1,token))
    c.execute("UPDATE 'tokens' SET 'opt2' =? WHERE 'token' =?",(choice2,token))
    c.execute("UPDATE 'tokens' SET 'opt3' =? WHERE 'token' =?",(choice3,token))
    conn.commit()

def add_choice(token,choice):
    """Register the chosen option into the database.  
    
    Keyword arguments:  
    token -> the choice's token  
    choice -> the made choice"""
    c.execute("UPDATE 'tokens' SET 'choice' =? WHERE 'token' =?",(choice,token))
    conn.commit()

def get_token_data(token):
    """Gain the info about a specific token  
    
    Keyword arguments:  
    token -> the token"""
    c.execute("SELECT * FROM 'tokens' WHERE 'token' =?",(token,))
    return c.fetchone()
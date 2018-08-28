from config import shop_file, general_database
import sqlite3
import json

conn = sqlite3.connect(general_database)
c = conn.cursor()

def get_shop_config(shop_file):
    with open(shop_file) as f:
        return json.load(f) # Load shop config file

def add_shop(message_id):
    """Add a new message as a shop to the database."""
    c.execute("INSERT INTO 'shops'('message') VALUES (?);",(int(message_id),))
    conn.commit()

def age_shop():
    """Let the shops become a little older, allowing the admins to distinguish old shops from new ones."""
    c.execute("UPDATE 'shops' SET age = age + 1;")
    conn.commit()

def purge_shop(age):
    """Delete all shops that have at least a given age."""
    c.execute("DELETE FROM 'shops' WHERE age > ?;",(age,))
    conn.commit()

def is_shop(message_id):
    """Returns a boolean on whether a given message is a shop or not."""
    c.execute("SELECT * FROM 'shops' WHERE 'message' =?;",(message_id,))
    if c.fetchall() == []:
        return False
    return True

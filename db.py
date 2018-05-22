import sqlite3
from config import database

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

if __name__ == "__main__":
    print get_user(1)

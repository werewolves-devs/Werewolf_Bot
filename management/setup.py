import sqlite3
from config import database

conn = sqlite3.connect(database)
c = conn.cursor()

def add_role(role,amount = 1):
    """Add a given amount of a given role to the role-pool.

    Keyword arguments:
    role -> the role that is added to the role-poll.
    amount -> how many of that role needs to be added."""

    c.execute("SELECT * FROM 'role-pool' WHERE role =?",(role,))
    if c.fetchall() == []:
        if amount <= 0:
            return

        c.execute("INSERT INTO 'role-pool' ('role','amount') VALUES (?,?)",(role,amount))
        conn.commit()
        return

    c.execute("UPDATE 'role-pool' SET amount = amount + ? WHERE role =?",(amount,role))
    c.execute("DELETE FROM 'role-pool' WHERE amount <= 0")
    conn.commit()

class Choice:
    def __init__(self,role,amount):
        self.amount = amount
        self.role = role

def view_roles(show_text=False):
    """Gives a list that displays all chosen roles in the database.

    Returns: a list of instances of the Choice class.
    """
    c.execute("SELECT  * from 'role-pool'")
    rows = c.fetchall()
    result = []
    for row in rows:
        result.append(Choice(role=row[0], amount=row[1]))

    result.sort()
    if not show_text:
        return result
    
    msg = ""
    for row in result:
        msg += "**{}** ".format(row.role)
        if row.amount > 1:
            msg += "*({}x)*".format(row.amount)
        msg += "\n"
    return msg
import sqlite3
import random
from config import general_database
from management.position import positionof
from management.db import db_set

conn = sqlite3.connect(general_database)
c = conn.cursor()

def add_activity(user_id,user_name):
    """Increase the activity score of a player."""
    c.execute("SELECT * FROM 'activity' WHERE id =?",(user_id,))
    if c.fetchone() == None:
        c.execute("INSERT INTO 'inventory'('id','name') VALUES (?,?);",(user_id,user_name))
        c.execute("INSERT INTO 'activity'('id','name') VALUES (?,?);",(user_id,user_name))
        c.execute("INSERT INTO 'users'('id','name') VALUES (?,?);",(user_id,user_name))
    c.execute("UPDATE 'activity' SET spam_activity = spam_activity + 1 WHERE id =?",(user_id,))
    conn.commit()
    db_set(user_id,'name',user_name)

def purge_activity():
    """Purge the activity score of all players."""
    c.execute("UPDATE activity SET spam_activity = 0 WHERE spam_activity > 2*spam_filter;")
    c.execute("UPDATE activity SET activity = activity + spam_activity*spam_activity/-spam_filter + 2*spam_activity;")
    c.execute("UPDATE activity SET activity = activity*0.9958826236;")
    c.execute("UPDATE activity SET spam_activity=0")
    c.execute("UPDATE activity SET record_activity = activity WHERE record_activity < activity;")

    c.execute("UPDATE users SET activity = (SELECT activity.activity FROM activity WHERE activity.id = users.id);")
    conn.commit()

def deal_credits():
    """Give all players a small portion of credits based on their activity."""
    c.execute("UPDATE users SET credits = credits + CAST( activity/500 AS INTEGER);")
    conn.commit()

def gain_leaderboard(user_id,amount=50):
    """Show a leaderboard for all players"""
    amount = min(amount,50)
    amount = max(1,amount)
    c.execute("SELECT * FROM 'activity' ORDER BY activity+spam_activity DESC;")
    result_table = []
    next_layer = c.fetchmany(amount)

    user_found = False
    for user in next_layer:
        if user[0] == user_id:
            user_found = True
    while next_layer != [] and not user_found:
        result_table.extend(next_layer)

        next_layer = c.fetchmany(amount)
        for user in next_layer:
            if user[0] == user_id:
                user_found = True
    result_table.extend(next_layer)
    result_table.extend(c.fetchmany(2))

    msg = "**Most active users:**\n\n"

    for i in range(min(amount,len(result_table))):
        element = result_table[i]
        msg += "**{}. {}** - {} points\n".format(i+1,element[1],int(element[2]) + int(element[3]))

    if len(result_table) > amount + 2:
        for i in range(len(result_table)):
            if result_table[i][0] == user_id:
                msg += "\n\n**__Your position:__**\n"
                if i > 1:
                    msg += "**{}. {}** - {} points\n".format(i-1,result_table[i-2][1],int(result_table[i-2][2])+int(result_table[i-2][3]))
                if i > 0:
                    msg += "**{}. {}** - {} points\n".format(i,result_table[i-1][1],int(result_table[i-1][2])+int(result_table[i-1][3]))
                msg += "**{}. {}** - {} points\n".format(i+1,result_table[i][1],int(result_table[i][2])+int(result_table[i][3]))
                if i < len(result_table) - 1:
                    msg += "**{}. {}** - {} points\n".format(i+2,result_table[i+1][1],int(result_table[i+1][2])+int(result_table[i+1][3]))
                if i < len(result_table) - 2:
                    msg += "**{}. {}** - {} points\n".format(i+3,result_table[i+2][1],int(result_table[i+2][2])+int(result_table[i+2][3]))

    return msg

def get_user(user_id):
    """Get all info about a user."""
    c.execute("SELECT * FROM 'users' WHERE id=?",(user_id,))
    return c.fetchone()

def get_credits(user_id):
    value = get_user(user_id)
    if value == None:
        return None
    return value[2]

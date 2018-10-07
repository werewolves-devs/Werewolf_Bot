from management.general import get_credits, set_credits
from management.items import item_to_int
import config
import sqlite3

conn = sqlite3.connect(config.general_database)
c = conn.cursor()

def take_item(user_id,item,amount=-1):
    try:
        number = int(item)
    except ValueError:
        number = item_to_int(item)
        if number == None:
            print('Failed to update inventory!')
            return None
    
    if number == 0:
        return set_credits(user_id,amount)

    c.execute("SELECT * FROM 'inventory' WHERE id=? AND item=?",(user_id,number))

    if c.fetchone() == None:
        c.execute("INSERT INTO 'inventory'('id','item','amount') VALUES (?,?,?);",(user_id,number,amount))
    else:
        c.execute("UPDATE 'inventory' SET amount = amount + ? WHERE item=?",(amount,number))
    c.execute("DELETE FROM 'inventory' WHERE amount =0")
    conn.commit()

def has_item(user_id,item,return_bool=True):
    try:
        number = int(item)
    except ValueError:
        number = item_to_int(item)
        if number == None:
            print('Failed to update inventory!')
            if return_bool:
                return False
            return 0

    if number == 0:
        return get_credits(user_id)

    c.execute("SELECT * FROM 'inventory' WHERE id=? AND item=?",(user_id,number))

    result = c.fetchone()
    if return_bool:
        if result == None:
            return False
        return True
    if result == None:
        return 0
    return int(result[2])

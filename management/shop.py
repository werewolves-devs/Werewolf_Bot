from management import items, inventory
import sqlite3
import config

conn = sqlite3.connect(config.general_database)
c = conn.cursor()

def __create_shop():
    c.execute("SELECT item, price FROM 'shops'")
    return [(int(item[0]), item[1]+0.5) for item in c.fetchall()]

def __item_traded_for_price(item,price):
    c.execute("UPDATE 'shops' SET bought = bought + 1 WHERE item=?",(item,))
    c.execute("UPDATE 'shops' SET price = (price + ?)/2 WHERE item=? AND bought > 1",(price,item))
    conn.commit()

def __refresh():
    c.execute("SELECT item, price, oldprice FROM 'shops' WHERE bought > 1;")
    changed_items = c.fetchall()

    c.execute("UPDATE 'shops' SET bought = 0")
    c.execute("UPDATE 'shops' SET oldprice = price")
    conn.commit()
    return [(int(item[0]), int(item[1]), int(item[2])) for item in changed_items if int(item[1]) != int(item[2])]

def get_market_message():
    msg_table = []
    msg = "**The Devil's Market:**\n"

    shop = __create_shop()

    for i in range(len(shop)):
        item = shop[i]
        item_name = items.int_to_item(item[0])
        price_to_buy = max(int(1.1 * item[1]),int(item[1])+1)
        price_to_sell = min(int(0.9 * item[1]),max(1,int(item[1]-1)))

        item_text = "**[{}]** {}\n**Buy:** {} credits.\n**Sell:** {} credits.\n\n".format(i+1,item_name,price_to_buy,price_to_sell)
        
        if len(msg+item_text) > 1950:
            msg_table.append(msg)
            msg = ""
        
        msg += item_text
    
    msg_table.append(msg)
    return msg_table

def buy(user_id,number):
    i = int(number) - 1
    shop = __create_shop()

    if i >= len(shop) or i < 0:
        return "Invalid value! Please choose a provided number!"

    item = shop[i]
    item_name = items.int_to_item(item[0])
    price_to_buy = max(int(1.1 * item[1]),int(item[1])+1)

    if inventory.has_item(user_id,0,False) < price_to_buy:
        return "I am sorry! You do not have enough credits to buy one {}!".format(item_name)
    
    inventory.give_item(user_id,item[0],1)
    inventory.give_item(user_id,0,-1*price_to_buy)

    __item_traded_for_price(item[0],price_to_buy)

    return "You have successfuly bought one {}!\nType `".format(item_name) + config.devil_prefix + "inventory` to view your inveentory."

def sell(user_id,number):
    i = int(number) - 1
    shop = __create_shop()

    if i >= len(shop) or i < 0:
        return "Invalid value! Please choose a provided number!"

    item = shop[i]
    item_name = items.int_to_item(item[0])
    price_to_sell = min(int(0.9 * item[1]),max(1,int(item[1]-1)))

    if not inventory.has_item(user_id,item[0]):
        return "I am sorry! You cannot sell one {} if you do not have one!".format(item_name)
    
    inventory.give_item(user_id,item[0])
    inventory.give_item(user_id,0,price_to_sell)

    __item_traded_for_price(item[0],price_to_sell)

    return "You have successfuly sold one {}!\nType `".format(item_name) + config.devil_prefix + "inventory` to view your inventory."

def refresh_market():
    return __refresh()


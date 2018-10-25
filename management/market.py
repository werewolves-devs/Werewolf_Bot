import sqlite3
import random
import config
import json

conn = sqlite3.connect(config.general_database)
c = conn.cursor()

def give_item(user_id,item,amount):
    item = __item_to_int(item)

    if item == 0:
        raise ValueError("Money is to be changed using the `self.money` argument.")

    c.execute("SELECT * FROM 'inventory' WHERE id=? AND item=?",(user_id,item))

    if c.fetchone() == None:
        c.execute("INSERT INTO 'inventory'('id','item','amount') VALUES (?,?,?);",(user_id,item,amount))
    else:
        c.execute("UPDATE 'inventory' SET amount = amount + ? WHERE item=? AND id=?",(amount,item,user_id))
    c.execute("DELETE FROM 'inventory' WHERE amount =0")
    conn.commit()

def take_item(user_id,item,amount):
    give_item(user_id,item,-amount)

def __jget(variable):
    jdict = json.loads(open(config.item_file).read())
    return jdict[variable]

def __jset(variable,value):
    with open(config.item_file, 'r') as f:
        jdict1 = json.load(f)
        jdict1[variable] = value
    with open(config.item_file, 'w') as f:
        json.dump(jdict1, f)

def __create_rewards(bonus=1):
    option_list = []

    common = __jget("common")
    rare = __jget("rare")
    epic = __jget("epic")
    legendary = __jget("legendary")

    # Normalize the numbers
    sum = common + rare + epic + legendary
    common = common/sum
    rare = rare/sum
    epic = epic/sum
    legendary = legendary/sum

    reward_list = __jget("rewards")

    for i in range(3):
        random_value = bonus*random.random()

        if random_value < legendary:
            option = random.choice(reward_list[3])
            option_list.append(option)
            reward_list[3].remove(option)
        elif random_value < epic + legendary:
            option = random.choice(reward_list[2])
            option_list.append(option)
            reward_list[2].remove(option)
        elif random_value < rare + epic + legendary:
            option = random.choice(reward_list[1])
            option_list.append(option)
            reward_list[1].remove(option)
        else:
            option = random.choice(reward_list[0])
            option_list.append(option)
            reward_list[0].remove(option)
    
    return option_list

def __import_reward_info(data_number):
    for rarity_list in __jget("rewards"):
        for item in rarity_list:
            if item["code"] == data_number:
                return item
    print("ERROR: Reward {} not found in {}!".format(data_number,config.item_file))
    return {'name': 'NOT FOUND!', 'code': data_number, 'description': 'Come \'n\' get your NOT FOUND! Who doesn\'t want a NOT FOUND? (Please report this)' }

def __item_to_int(title):
    try:
        int(title)
    except ValueError:
        for item in __jget("items"):
            if item["name"] == title:
                return item["code"]
        return None
    else:
        return int(title)

def __item_to_name(number):
    for item in __jget("items"):
        if item["code"] == number:
            return item["name"]
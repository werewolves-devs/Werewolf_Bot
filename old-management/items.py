import random
import config
import json

def jget(variable):
    """Return what value the given variable is set to. Note that the parameter variable needs to be a string.
    
    Keyword arguments:
    variable -> the variable in dynamic.json that should be changed."""
    
    jdict = json.loads(open(config.item_file).read())
    return jdict[variable]

def jset(variable,value):
    """Change the variable in the dynamic config to the given value.
    
    Keyword arguments:
    variable -> the variable that should be changed.  
    value -> the value the variable should be set to."""
    
    with open(config.item_file, 'r') as f:
        jdict1 = json.load(f)
        jdict1[variable] = value
    with open(config.item_file, 'w') as f:
        json.dump(jdict1, f)

def get_rewards(bonus=1):
    option_list = []

    common = jget("common")
    rare = jget("rare")
    epic = jget("epic")
    legendary = jget("legendary")

    # Normalize the numbers
    sum = common + rare + epic + legendary
    common = common/sum
    rare = rare/sum
    epic = epic/sum
    legendary = legendary/sum

    reward_list = jget("rewards")

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

def import_reward(data_number):
    for rarity_list in jget("rewards"):
        for item in rarity_list:
            if item["code"] == data_number:
                return item
    print("ERROR: Reward {} not found in {}!".format(data_number,config.item_file))
    return {'name': 'NOT FOUND!', 'code': data_number, 'description': 'Come \'n\' get your NOT FOUND! Who doesn\'t want a NOT FOUND? (Please report this)' }

def item_to_int(title):
    for item in jget("items"):
        if item["name"] == title:
            return item["code"]
    return None

if  __name__ == '__main__':
    print(jget("items"))
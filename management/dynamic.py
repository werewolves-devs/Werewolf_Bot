# This file's meaning is to open the dynamic config, and distribute it to whomever needs its information
from config import dynamic_config
import json

def jget(variable):
    """Return what value the given variable is set to. Note that the parameter variable needs to be a string.
    
    Keyword arguments:
    variable -> the variable in dynamic.json that should be changed."""
    
    jdict = json.loads(open(dynamic_config).read())
    return jdict[variable]

def jset(variable,value):
    """Change the variable in the dynamic config to the given value.
    
    Keyword arguments:
    variable -> the variable that should be changed.  
    value -> the value the variable should be set to."""
    
    with open(dynamic_config, 'r') as f:
        jdict1 = json.load(f)
        jdict1[variable] = value
    with open(dynamic_config, 'w') as f:
        json.dump(jdict1, f)
    
def get_stage():
    """Return what stage the game is currently in"""
    return jget("stage")

def set_stage(value):
    """Change the stage of the game to the given value.
    
    Keyword arguments:  
    value -> the value the game stage should be changed into.  
    
    Valid arguments are 'Day', 'Night' and 'NA'."""
    
    if value in ['Day','Night','NA']:
        return jset("stage",value)

    raise ValueError("Attempt made to set stage to invalid value: {}".format(value))

    # Day - daytime
    # Night - nighttime
    # NA - out of game/otherwise

def day_number():
    """Return the game's current day number"""
    return int(jget("day"))

def next_day():
    """Set the game's current day one step forward."""
    return jset("day",day_number()+1)

def reset_day():
    """Reset the day number to start the game."""
    return jset("day",-1)

def get_mayor():
    """Get the id of the town's current mayor"""
    return jget("Mayor")

def set_mayor(user_id):
    """Set the mayor to the given id  
    
    userid -> the id of the user that is to be set mayor"""
    return jset("Mayor",user_id)

def kill_mayor():
    """Remove the mayor from the dynamic config file. The town will now longer have a mayor.  """
    return set_mayor(0)

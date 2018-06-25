# This file's meaning is to open the dynamic config, and distribute it to whomever needs its information
from config import dynamic_config
import json

def jget(variable):
    """Return what value the given variable is set to. Note that the parameter variable need to a string.
    
    Keyword arguments:
    variable -> the variable in dynamic.json that should be changed."""

    jdict = json.loads(open(dynamic_config).read())
    return jdict[variable]

def jset(variable,value):
    """Change the variable in the dynamic config to the given value.
    
    Keyword arguments:
    variable -> the variable that should be changed.  
    value -> the value the variable should be set to."""

def get_stage():
    """Return what stage the game is currently in"""
    return jget("stage")

def set_stage(value):
    """Change the stage of the game to the given value.
    
    Keyword arguments:  
    value -> the value the game stage should be changed into.  
    
    Valid arguments are 'Day', 'Night' and 'NA'."""

    # Day - daytime
    # Night - nighttime
    # NA - out of game/otherwise

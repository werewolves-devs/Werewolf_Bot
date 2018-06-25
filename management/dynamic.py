# This file's meaning is to open the dynamic config, and distribute it to whomever needs its information
from config import dynamic_config

def jget(variable):
    """Return what value the given variable is set to.
    
    Keyword arguments:
    variable -> the variable in dynamic.json that should be changed."""

    # TODO
    # The variable dynamic_config contains the name of the dynamic JSON-formatted config.

    return #TODO

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

# How this works

This folder contains all the management with the database directly, or, possibly later on, with the self-built API. You can use it in any Python file that is connected with the bot.

## Relevant files

The folder contains a few files. Here's an explanation of what everything is and what it all does.

### __init__.py
This file is merely to add the folder to the PYTHONPATH and have it seen as a module. This means that ./management can be imported as a package (management)

### db.py
This is the relevant file that contains all the commands you need. If one wishes to import these functions, one could either use
    import management.db as db
    db.execute("SELECT * FROM game")
or one could work with the commands like
    from management.db import emoji_to_player, get_user
    emoji_to_player(":smirk:") # Invalid emoji, but irrelevant for the example

#### execute(command)
This command is used if one directly wishes to use a command upon the SQL database. Use of this function is discouraged, as it may not always be SQL-injection proof.

#### emoji_to_player(emoji)
The **emoji_to_player()**-function takes a given emoji as an input and looks through the database if there's a participant with that emoji. This function is resistant to SQL-injection, and returns a user's id if it has found a match, and returns None if it cannot find a participant.

#### get_user(id)
Gather all information of a participant. However, this information is still unparsed, and using **db_get()** where possible is encouraged.

#### db_get(user_id,column)
Find a certain aspect of a user's 

def channel_introduction(role):
    '''
    Do it like this:
    '''
    if role == "": # insert role here
        msg = "Hi! This is your channel! " # The first one is without a plus
        msg += "All the cool stuff happens in here! " # But all the others are with a plus
        msg += "**I can still use ordinary Discord layout** _as you can see._ "
        msg += "So yeah, that's pretty cool, huh?\n" # End lines with \n
        msg += "I hope you enjoy. We do!"
    '''
    See? Not so difficult, huh?
    '''
    
    
    if role == "Assassin":
        msg = "**=========================\n"
        msg += "**WELCOME, ASSASSIN\n"
        msg += "**=========================**\n"
        msg += "This town is like an old kitchen... it's a giant mess. Luckily, the town has *you*, "
        msg += "their protector, who picks out the cockroaches for them and squishes them like the puny animals they are. "
        msg += "You do not exactly know what is about to happen, but your senses never lie; "
        msg += "something *TERRIBLE* is happening, and it depends on your actions how much the town will suffer from it!\n"
        msg += "You do not know your allies, your masters taught you never to trust anyone. However, "
        msg += "you fear you can't do this alone. You must find the ones to save, and especially the ones to kill."
        msg += "**You are the assassin. Each night (except for the first one), you can attack and kill a player you suspect. "
        msg += "Play the game whichever way you'd like, but try to keep the innocents alive. Good luck.**"
    
    # Ignore this. This allows us to see your message.
    return msg

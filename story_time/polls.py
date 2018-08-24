import random

def story_text(purpose):
    msg_table = []

    # All existing poll purposes
    #
    # wolf
    # cult
    # thing
    # lynch
    # Mayor
    # Reporter
    #
    # Max. story size is 512 characters

    if purpose == 'wolf':
        msg = 'Rawr.'
        msg_table.append(msg)

        msg = 'Nom nom.'
        msg_table.append(msg)

        msg = "**WOLVES**\nThe time to still your hunger has arrived! Whom shall you eat tonight?"
        msg_table.append(msg)

        msg = "Nom nom? Nom nom."
        msg_table.append(msg)

        msg = "Those filthy fruits that the villagers eat... ugh! You try to eat those, but you know that there's only one thing that can truly release you from your hunger; *MEAT!*"
        msg_table.append(msg)

        msg = "**WOLVES!**\nThe time to eat, has arrived! Who shall it be?"
        msg_table.append(msg)

        msg = "Whom shall you devour tonight?"
        msg_table.append(msg)

        msg = "Is it time? **IT IS TIME!** At last, you can eat somebody. Hopefully it\'s gonna be a fat one..."
        msg_table.append(msg)

    if purpose == 'cult':
        msg = "Let the leader approve of this! The time to kill a victim has come!"
        msg_table.append(msg)

        msg = "Too much blood has been spoiled in this town! Let's end this by... spoiling MORE blood!"
        msg_table.append(msg)

        msg = "Dear cult, the time to visit a victim has arrived! Whom shall you execute tonight?"
        msg_table.append(msg)

        msg = "**CULT MEMBERS!** Your leader has given you the task to kill... kill whom exactly?"
        msg_table.append(msg)

        msg = "The day has ended, but sadly the killing spree hasn't. Will you put an end to this tonight?"
        msg_table.append(msg)

        msg = "\"Hi, it's your neighbours! Could you open the door? We just need a little bit of sugar!\" That\'ll be your strategy tonight. All you need to figure out, is upon whom you shall use this."
        msg_table.append(msg)

        msg = "The time has come to cleansen this town of the one who has caused it all! But who exactly is that one?"
        msg_table.append(msg)

        msg = "Tonight\'s a busy night. You have all come together to decide if you wish to get rid of someone, and, if so, who it is that shall be killed!"
        msg_table.append(msg)

    if purpose == 'thing':
        msg = "What monstruous creature is hiding in the swamp? Let\'s sacrifice each other, maybe that\'ll get it satisfied!"
        msg_table.append(msg)

        msg = "*\"I heard the creature was secretly one of us! We gotta find the monster and kill it!\"*"
        msg_table.append(msg)

        msg = "Where is the monster? WHO IS IT?"
        msg_table.append(msg)

        msg = "Sooo.... the thing isn\'t dead yet? Let\'s kill it tonight!"
        msg_table.append(msg)

        msg = "Is... is it gone?"
        msg_table.append(msg)

        msg = "\"I've seen it! I've seen that... thing! Look, over there! Throw some rocks at it!\""
        msg_table.append(msg)

    if purpose == 'lynch':
        msg = "Last night was a terrific night! Some didn\'t sleep well, while others didn\'t sleep at all! Someone must pay for this!"
        msg_table.append(msg)

        msg = "The town got fed up with the weird surrounding mist! It\'s about time that whoever or whatever causes it, comes to and end today!"
        msg_table.append(msg)

        msg = "The town decided to have a brutal public execution at the end of the day! Everything\'s prepared and all ready, now we just need to choose a victim."
        msg_table.append(msg)

        msg = "The town had enough of whatever\'s happening. It\'s time we find the guilty person."
        msg_table.append(msg)
        
    return msg_table[random.randint(0,len(msg_table)-1)]

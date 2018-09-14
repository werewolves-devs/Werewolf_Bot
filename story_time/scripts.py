import random as randium

class Conversation:
    def __init__(self,content,bot,time):
        """
        Bot value:  
        0 -> Werewolf Bot  
        1 -> Time Bot  
        2 -> Ghost Bot  
        3 -> Devil Bot"""
        self.content = content
        self.time = time
        self.bot = bot

def welcome(user_id,number=-1):
    script_table = []

    msg_table = []
    msg_table.append(Conversation("Hey there! Welcome, <@{}>!".format(user_id),2,0))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("Right on time! Glad to have ya here, <@{}>.".format(user_id),1,0))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("Arrroooo! Welcome to the Werewolves server, <@{}>!".format(user_id),0,0))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("Another soul! Another soul!",3,0))
    msg_table.append(Conversation("Welcome, <@{}>. Please make yourself comfortable, for as long as you can...".format(user_id),3,2))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("My goodness! Look who it is!",0,0))
    msg_table.append(Conversation("What, is that <@{}>? **THE** <@{}>?".format(user_id),2,2))
    msg_table.append(Conversation("Lemme talk to him! Lemme talk to him! Pleeeease!",0,1))
    msg_table.append(Conversation("I'm sorry, you know the rules.",2,2))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("Oh god, **ANOTHER** random person. Get lost, <@{}>!".format(user_id),0,0))
    msg_table.append(Conversation("Excuse me? Is that your new attitude to new people now? Get yourself together!",2,2))
    msg_table.append(Conversation("I kinda like that attitude.",3,3))
    msg_table.append(Conversation("**ANYWAY,** hey there, <@{}>. Welcome to the Werewolf server!".format(user_id),3,1))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("Oh, hey, <@{}>! Glad to see ya around!".format(user_id),0,0))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("Wait, what just happened?",1,0))
    msg_table.append(Conversation("Ho god, did somebody just join again? Erm, whose turn is it now?",0,2))
    msg_table.append(Conversation("*Pssst! Wrong channel! This one can be read by humans.*",2,4))
    msg_table.append(Conversation("You're right! Quick, act like you don't have a self-consciousness!",1,2))
    msg_table.append(Conversation("Beep boop! Welcome to the server, <@{}>!".format(user_id),0,0))
    msg_table.append(Conversation("Beep boop! Welcome to the server, <@{}>!".format(user_id),1,0))
    msg_table.append(Conversation("Beep boop! Welcome to the server, <@{}>!".format(user_id),2,0))
    msg_table.append(Conversation("Beep boop! Welcome to the server, <@{}>!".format(user_id),3,0))
    script_table.append(msg_table)

    msg_table = []
    msg_table.append(Conversation("Eyyyyy! Look who's here!",2,0))
    msg_table.append(Conversation("Who's here?",1,2))
    msg_table.append(Conversation("Is it a bird?",0,2))
    msg_table.append(Conversation("Is it a plane?",1,2))
    msg_table.append(Conversation("No, it's <@{}>! Welcome, buddy!",2,2))
    script_table.append(msg_table)

    if number == -1:
        return len(script_table)
    return script_table[randium.randint(0,len(script_table)-1)]
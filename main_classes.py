import roles
from config import game_log

# This class is being used to pass on to above. While the administration is done underneath the hood, messages are passed out to give the Game Masters and the players an idea what has happened.
class Mailbox:
    def __init__(self):
        self.gamelog = []
        self.botspam = []
        self.storytime = []
        self.channel = []
        self.player = []
    
    def log(self,message):
        self.gamelog.append(message)
    def log_add(self,message):
        if len(self.gamelog) > 0:
            self.gamelog[-1] += message
            return
        print("Attempted to add message to non-existent game-log message!\n{}".format(message))
        
    def spam(self,message):
        self.botspam.append(message)
    def spam_add(self,message):
        if len(self.botspam) > 0:
            self.botspam[-1][1] += message
            return
        print("Attempted to add message to non-existent bot-spam message!\n{}".format(message))
        
    def story(self,message):
        self.storytime.append(message)
    def story_add(self,message):
        if len(self.storytime) > 0:
            self.storytime[-1] += message
            return
        print("Attempted to add message to non-existent story-time message!\n{}".format(message))
    
    def respond(self,message,channel):
        self.channel.append([message,channel])
    def respond_add(self,message):
        if len(self.channel) > 0:
            self.channel[-1][0] += message
            return
        print("Attempted to add message to non-existent response!\n{}".format(message))

    def dm(self,message,channel):
        self.player.append([message,channel])
    def dm_add(self,message):
        if len(self.player) > 0:
            self.player[-1][0] += message
            return
        print("Attempted to add message to non-existent DM!\n{}".format(message)) 

    # Gain all info from another mailbox and put them inside this one.
    def suck(self,old_mail):
        for msg in old_mail.gamelog:
            self.log(msg)
        for msg in old_mail.botspam:
            self.spam(msg)
        for msg in old_mail.storytime:
            self.story(msg)
        for parcel in old_mail.channel:
            self.channel.append(parcel)
        for parcel in old_mail.player:
            self.player.append(parcel)   

# This class contains all information that needs to be global. It is used for retrieving and passing on information from different functions.
class Game_Control:
    
    # All attacks are listed in here, including the role that attacked them.
    kill_queue = []

    # The time in the game. Either "Day", "Night" or "Undefined"
    time = "Undefined"

    # This command is executed when the day is started.
    def start_day(self):
        self.time = "Day"
    
    # This command is executed when the night is started.
    def start_night(self):
        self.time = "Night"
    
    # Unsure if this will have a purpose.
    def pause(self):
        self.time = "Undefined"
        

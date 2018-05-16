from roles import Spectator

class Participant:

    # This is a universal table among all participants to figure out the position of each participant in the upper table.
    idTable = []
    
    def __init__(self,name,id,channel):
        self.name = name
        self.role = Spectator()
        self.id = id
        self.channel = channel # The personal channel of the player, where their special powers will trigger.
        
        self.fakerole = self.role.name # The tanner's role.

        # List of roles that can kill this player
        self.killers = []

        # Set up abilities
        self.uses = 0
        self.votes = 1
        self.threatened = 0

        # Set up special conditions
        self.enchanted = False
        self.demonized = False
        self.powdered = False
        self.frozen = False
        self.undead = False
        self.bites = 0
        self.bitten = False

        # Set up lists of people to kill or to sleep with
        self.lovers = []
        self.zombies = []
        self.sleepers = []

        # Set up the inventory of the player
        self.souls = -1
        self.amulets = []
        
        # Keep track of how many hours the participant hasn't said anything.
        self.activity = 0
    
    # Take care of a participant's activity
    def hour(self):
        self.activity += 1
        if self.activity == 48:
            # GIVE A WARNING
            # TODO
        if self.activity == 72:
            # GIVE A NOTIFICATION
            # TODO
    def talk(self):
        self.activity = 0

# This class is being used to pass on to above. While the administration is done underneath the hood, messages are passed out to give the Game Masters and the players an idea what has happened.
class Mailbox:
    def __init__(self):
        self.gamelog = []
        self.botspam = []
        self.response = []
        self.dmcaster = []
        self.dmvictim = []
    
    def log(self,message):
        self.gamelog.append(message)
    def log_add(self,message):
        if len(self.gamelog) > 0:
            self.gamelog[-1] += message
            return
        print("Attempted to add message to non-existent message!\n{}".format(message))
        
    def spam(self,message):
        self.botspam.append(message)
    def spam_add(self,message):
        if len(self.botspam) > 0:
            self.botspam[-1] += message
            return
        print("Attempted to add message to non-existent message!\n{}".format(message))
        
    def answer(self,message):
        self.response.append(message)
    def answer_add(self,message):
        if len(self.response) > 0:
            self.response[-1] += message
            return
        print("Attempted to add message to non-existent message!\n{}".format(message))
    
    def dmcaster(self,message):
        self.dmcaster.append(message)
    def dmcaster_add(self,message):
        if len(self.dmcaster) > 0:
            self.dmcaster[-1] += message
            return
        print("Attempted to add message to non-existent message!\n{}".format(message))

    def dmvictim(self,message):
        self.dmvictim.append(message)
    def dmvictim_add(self,message):
        if len(self.dmvictim) > 0:
            self.dmvictim[-1] += message
            return
        print("Attempted to add message to non-existent message!\n{}".format(message))

# This class contains all information that needs to be global. It is used for retrieving and passing on information from different functions.
class Game_Control:
    
    # All attacks are listed in here, including the role that attacked them.
    kill_queue = []
    
    # In here, all participants are listed.
    participants = []

    # This command locates the position of a selected player in the participants table.
    def position(self,victim_id):
        for i in len(self.participants):
            if participants[i].id == victim_id:
                return i
        print("The location has been requested of a participant that doesn't exist!")
        return False
    
    # This command adds a victim to the kill_queue.
    def add_kill(self,victim_id,murderer):
        self.kill_queue.append([self.position(victim_id),murderer])


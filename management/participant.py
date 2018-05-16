from roles import Spectator

class Participant:

    # This is a universal table among all participants to figure out the position of each participant in the upper table.
    idTable = []
    
    def __init__(self,name,id,channel):
        self.name = name
        self.role = Spectator()
        self.id = id
        self.channel = channel # The personal channel of the player, where their special powers will trigger.

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
    def spam(self,message):
        self.botspam.append(message)

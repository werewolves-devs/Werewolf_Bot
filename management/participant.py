from roles import Spectator

class Participant:

    # This is a universal table among all participants to figure out the position of each participant in the upper table.
    idTable = []
    
    def __init__(self,name,id):
        self.name = name
        self.id = id
        self.role = Spectator(id,"0")
        
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

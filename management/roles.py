class Spectator:

    def __init__(self,personal_channel):
        self.name = "Spectator"
        self.channel = personal_channel

        # Set up special conditions
        self.enchanted = False
        self.demonized = False
        self.powdered = False
        self.frozen = False
        self.undead = False

        # Set up lists of people to kill etc.
        self.lovers = []
        self.zombies = []
        self.sleepers = []

        # Set up the inventory of the player
        self.souls = -1
        self.amulets = []

# ===============================================
class Innocent(Spectator):

    def __init__(self,name,id,channel,uses,votes,threatened,enchanted,demonized,powdered,frozen,undead,lovers,zombies,sleepers,souls,amulets):
        self.name = name
        self.id = id
        self.channel = channel

        # Set up abilities
        self.uses = uses
        self.votes = votes
        self.threatened = threatened

        # Set up special conditions
        self.enchanted = enchanted
        self.demonized = demonized
        self.powdered = powdered
        self.frozen = frozen
        self.undead = undead

        # Set up lists of people to kill or to sleep with
        self.lovers = lovers
        self.zombies = zombies
        self.sleepers = sleepers

        # Set up the inventory of the player
        self.souls = souls
        self.amulets = amulets
    
    def power(self):
        pass
    
    def night(self):
        self.votes = 1
    
    def day(self):
        pass

# ===============================================
class Alcoholic(Innocent):
    pass

# ===============================================
class Amulet_Holder(Innocent):

    def power(self,playertable,victim):
        if self.uses > 0:
            for player in playertable:
                if victim.id == player.role.id and player.role.name not in ["Spectator", "Dead"]:
                    player.role.amulets.append(self.id)
                    return True
        return False
                    
    def night(self,playertable):
        self.votes = 1
        for player in playertable:
            if self.id in player.role.amulets and player.role.name == "Dead":
                player.role.amulets.remove(self.id)
                self.uses += 1

# ===============================================
class Assassin(Innocent):

    def power(self,playertable,victim):
        if self.uses > 0:
            for player in playertable:
                if victim.id == player.role.id and player.role.name not in ["Spectator", "Dead"]:
                    self.uses += -1
                    # TODO: add victim to kill queue
                    return True
        return False

    def night(self):
        self.votes = 1
        self.uses = 1
    
    def day(self):
        self.uses = 0

# ===============================================
class Aura_Teller(Assassin):

    #TODO
    pass

# ===============================================
class Baker(Innocent):
    pass

# ===============================================
class Butcher(Innocent):
    pass

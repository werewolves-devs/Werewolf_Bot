class Spectator:

    def __init__(self,id,personal_channel):
        self.name = "Spectator"
        self.id = id
        self.channel = personal_channel

        # Set up special conditions
        self.enchanted = False
        self.demonized = False
        self.powdered = False
        self.frozen = False
        self.undead = False
        self.bites = 0
        self.bitten = False

        # Set up lists of people to kill etc.
        self.lovers = []
        self.zombies = []
        self.sleepers = []

        # Set up the inventory of the player
        self.souls = -1
        self.amulets = []

# ===============================================
class Innocent(Spectator):
    
    def power(self):
        pass
    
    def night(self):
        self.votes = 1
    
    def day(self):
        self.bitten = False
    
    def kill(self,murderer):
        if murderer not in self.killers:
            return False
    
    def death_phase(self,murderer):
        if len(self.amulets) > 0 and self.name not in ["Amulet Holder", "Town Elder"]:
            return "Amulets"
        

# ===============================================
class Alcoholic(Innocent):
    pass

# ===============================================
class Amulet_Holder(Innocent):

    def power(self,playertable,victim):
        if self.uses > 0 and self.undead == False:
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
        if self.uses > 0 and self.undead == False:
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
        self.bitten = False

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

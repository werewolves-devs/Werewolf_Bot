from main_management import Mailbox, Game_Control

class Spectator:

    # NOTE: The spectator class is not meant for spectating!
    # Maybe a rename will be useful soon, but the Spectator is supposed to be a role-less participant.
    def __init__(self):
        self.name = "Spectator"

# ===============================================
class Innocent(Spectator):
    
    def __init__(self):
        self.name = "Innocent"
    
    def power(self,me):
        pass
    
    def night(self,me):
        me.votes = 1
    
    def day(self,me):
        me.bitten = False
        me.fakerole = self.name
    
    def standard_kill(self,me,murderer):
        if murderer == "Innocent":
            mail = Mailbox().log("The **{}** <@{}> got lynched by the town.".format(self.name,me.id))
            return mail.log_add(death_phase(me,murderer))
        if murderer == "Assassin":
            mail = Mailbox.log(" has attacked <@{}>.".format(me.id))
            return mail #TODO
    
    def death_phase(self,me,murderer):
        msg = ""

# ===============================================
class Alcoholic(Innocent):

    def __init__(self):
        self.name = "Alcoholic"
        self.killers = ["Innocent", "Assassin", "Barber", "Cult Leader", "Executioner", "Huntress", "Witch", "Werewolf", "Lone Wolf", "Devil", "Wager", "Horseman", "Pyromancer"]


# ===============================================
class Amulet_Holder(Innocent):

    def __init__(self):
        self.name = "Amulet Holder"
        self.killers = ["Innocent", "Assassin", "Barber", "Cult Leader", "Executioner", "Huntress", "Witch", "Werewolf", "Lone Wolf", "Devil", "Wager", "Horseman", "Pyromancer"]
        
    def power(self,me,playertable,victim):
        if me.uses > 0 and me.undead == False and me.id != victim.id:
            for player in playertable:
                if victim.id == player.id and player.role.name not in ["Spectator", "Dead"]:
                    player.amulets.append(self.id)
                    return True
        return False
                    
    def night(self,me,playertable):
        self.votes = 1
        for player in playertable:
            if me.id in player.amulets and player.role.name == "Dead":
                player.amulets.remove(self.id)
                self.uses += 1

# ===============================================
class Assassin(Innocent):

    def __init__(self):
        self.name = "Assassin"
        self.killers = ["Innocent", "Assassin", "Barber", "Cult Leader", "Executioner", "Huntress", "Witch", "Werewolf", "Lone Wolf", "Devil", "Wager", "Horseman", "Pyromancer"]
        
    def power(self,me,playertable,victim):
        if me.uses > 0 and me.undead == False:
            for player in playertable:
                if victim.id == player.id and player.role.name not in ["Spectator", "Dead"]:
                    me.uses += -1
                    # TODO: add victim to kill queue
                    return True
        return False

    def night(self,me):
        me.votes = 1
        me.uses = 1
    
    def day(self,me):
        me.uses = 0
        me.bitten = False

# ===============================================
class Aura_Teller(Assassin):

    def __init__(self):
        self.name = "Aura Teller"
        self.killers = ["Innocent", "Assassin", "Barber", "Cult Leader", "Executioner", "Huntress", "Witch", "Werewolf", "Lone Wolf", "Devil", "Wager", "Horseman", "Pyromancer"]

    #TODO: Add a function that returns one's aura.
    def power(self,me):
        pass

# ===============================================
class Baker(Innocent):
    
    def __init__(self):
        self.name = "Baker"
        self.killers = ["Innocent", "Assassin", "Barber", "Cult Leader", "Executioner", "Huntress", "Witch", "Werewolf", "Lone Wolf", "Devil", "Wager", "Horseman", "Pyromancer"]

# ===============================================
class Butcher(Innocent):
    
    def __init__(self):
        self.name = "Butcher"
        self.killers = ["Innocent", "Assassin", "Barber", "Cult Leader", "Executioner", "Huntress", "Witch", "Werewolf", "Lone Wolf", "Devil", "Wager", "Horseman", "Pyromancer"]

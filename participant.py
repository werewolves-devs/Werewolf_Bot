class Participant:

    # Keep universally track of all participants, to know their location in the global table.
    player_ids = []

    def __init__(self,id,personal_channel):
        # Let the participants know each other's position
        self.player_ids.append(id)
    
        # Set up personal information
        self.id = id
        self.role = "Spectator"
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

    # Determine if the player is going to be killed.
    def kill(self,murderer):
        # Players cannot die while frozen.
        if self.frozen == True:
            return "Frozen"

        # Make sure some unintended roles cannot accidentaly turn undead
        if self.role in ["Exorcist", "Demon", "Devil", "Vampire"] or self.undead == True:
            self.demonized == False
        # Make sure the pyromancer cannot kill themselves when powdered
        if self.role == "Pyromancer":
            self.powdered = False
        # Turn them if they're a cursed civilian and they caught attacked by wolves.
        if self.role == "Cursed Civilian" and murderer in ["Werewolf", "Lone Wolf"]:
            self.role = "Werewolf"
            return "Werewolf"
        # Turn them normal if they're a runner and they got attacked by wolves.
        if self.role == "Runner" and murderer in ["Werewolf", "Lone Wolf"]:
            self.role = "Innocent"
            return "Innocent"
        # If a wolf team member got attacked by a priest, ignore their status and kill them already.
        if murderer == "Priest" and self.role in ["Werewolf", "Bloody Butcher", "Curse Caster", "Hell Hound", "Infected Wolf", "Lone Wolf", "Sacred Wolf", "Tanner", "Warlock", "White Werewolf", "Wolf's Cub"]:
            self.role = "Dead"
            return "Dead"
        # If they die because a lover did, ignore their status and kill them already.
        if murderer == "Cupid":
            self.role = "Dead"
            return "Dead"

        # If none of these apply, just kill them.
        if murderer == "Pyromancer" and self.powdered == True:
            return self.death_phase(murderer)
        if murderer == "Assassin":
            return self.death_phase(murderer)
        if murderer == "Cult Leader":
            return self.death_phase(murderer)
        

    # Kill the player, but check if they can be saved first. If not, kill them.
    def death_phase(self,murderer):
        if len(self.amulets) > 0 and murderer not in ["Innocent", "Barber"]:
            return "Amulet"

        if self.souls > 0:
            self.souls += -1
            return "Soul"

        if self.demonized == True and murderer not in ["Innocent", "Barber", "Priest", "Exorcist"]:
            self.undead = True
            self.demonized = False
            return "Undead"

        self.role = "Dead"
        return "Dead"

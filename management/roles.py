from main_manage import Mailbox, Game_Control
from story_time.barber_kills import barber_kill_story

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
        me.threatened = 0
    
    def day(self,me):
        me.bitten = False
        me.fakerole = self.name
    
    def kill(self,me,murderer):
        if murderer == "Barber":
            pass
            
    def suicide(self,me):
        pass

# ===============================================
class Alcoholic(Innocent):

    def __init__(self):
        self.name = "Alcoholic"


# ===============================================
class Amulet_Holder(Innocent):

    def __init__(self):
        self.name = "Amulet Holder"
        
    def power(self,me,playertable,victim):
        if me.uses > 0 and me.undead == False and me.id != victim.id:
            for player in playertable:
                if victim.id == player.id and player.role.name not in ["Spectator", "Dead"]:
                    player.amulets.append(me.id)
                    return True
        return False
                    
    def night(self,me,playertable):
        me.votes = 1
        me.threatened = 0
        for player in playertable:
            if me.id in player.amulets and player.role.name == "Dead":
                player.amulets.remove(me.id)
                me.uses += 1

# ===============================================
class Assassin(Innocent):

    def __init__(self):
        self.name = "Assassin"
        
    def power(self,me,victim):
        if me.undead == True:
            return Mailbox().respond("I'm sorry, buddy! Now that you've become undead, you have lost your power to kill!",me.channel)
        if me.uses > 0:
            for player in Game_Control().participants:
                if victim.id == player.id and player.role.name not in ["Spectator", "Dead"]:
                    me.uses += -1
                    Game_Control().add_kill(victim.id,"Assassin",Mailbox().respond("The **Assassin** <@{}> has attacked".format(me.id),me.channel))
                    return Mailbox().respond("Target chosen! Tonight, you shall attack <@{}>!".format(victim.id),me.channel)
            return Mailbox().respond("I am terribly sorry! For some reason, I couldn't find your target.",me.channel)
        return Mailbox().respond("I'm sorry, bud! You can't use your power. Not now...",me.channel)

    def night(self,me):
        me.votes = 1
        me.uses = 1
        me.threatened = 0
    
    def day(self,me):
        me.fakerole = self.name
        me.uses = 0
        me.bitten = False

# ===============================================
class Aura_Teller(Assassin):

    def __init__(self):
        self.name = "Aura Teller"

    def power(self,me,victim):
        if me.undead == True:
            return Mailbox().respond("I'm sorry, man! Aura Tellers lose their powers once they turn undead!",me.channel)
        if me.uses > 0:
            if me.id == victim.id:
                return Mailbox().respond("I'm sorry, buddy! Suicide is not an option. Choose again!",me.channel)

            for player in Game_Control().participants:
                if victim.id == player.id and player.role.name not in ["Spectator", "Dead"]:
                    me.uses += -1
                    if player.role.name in ["Werewolf", "Bloody Butcher", "Hell Hound", "Infected Wolf", "Sacred Wolf", "White Werewolf", "Wolf's Cub"]:
                        mail = Mailbox().respond("{} - <@{}> appears to you as a **Threat**!".format(player.emoji,player.id),me.channel)
                        mail.respond("This means they're part of the wolf pack!",me.channel)
                        return mail.log("The **Aura Teller** <@{}> has inspected <@{}>, a **{}**, and discovered them as a threat!".format(me.id,player.id,player.role.name))
                    Mailbox().respond("{} - <@{}> does **not** appear to you as a threat.".format(player.emoji,player.id),me.channel)
                    return mail.log("The **Aura Teller** <@{0}> has inspected <@{1}>. As <@{1}> is a **{2}**, they did not appear as a threat to them.".format(me.id,player.id,player.role.name))
            return Mailbox().respond("Sorry, who could tell that I couldn't find your target?",me.channel)
        return Mailbox().respond("Sorry, buddy. You can't use your powers right now.",me.channel)

# ===============================================
class Baker(Innocent):
    
    def __init__(self):
        self.name = "Baker"

# ===============================================
class Butcher(Innocent):
    
    def __init__(self):
        self.name = "Butcher"

# ===============================================
class Barber(Innocent):

    def __init__(self):
        self.name == "Barber"
    
    def night(self,me):
        me.uses = 0
        me.votes = 1
        me.threatened = 0
    
    def day(self,me):
        me.uses = 1
        me.fakerole = self.name
        me.bitten = False
    
    def power(self,me,victim):
        if me.undead == True:
            return Mailbox().respond("You're undead! You can't use your powers!",me.channel)
        if me.uses > 0:
            if me.id == victim.id:
                return Mailbox().respond("Whether suicide is an option or not is for you to find out. However, it is not in this game. Try again, please.",me.channel)
            for player in Game_Control().participants:
                if player.id == victim.id and player.role.name not in ["Spectator", "Dead"]:
                    mail = Mailbox().log("The **Barber** <@{}> has chosen to assassinate".format(me.id))
                    if player.souls > 0:
                        mail.log_add(" <@{}>, a soulless **{}** who happened to have a soul protecting them.".format(player.id,player.role.name))
                        mail.respond("Though you thought you had cut up your target nicely enough, it seems they have somehow survived! Too bad...",me.channel)
                        return mail
                    mail.log_add(" <@{}>, the town's favourite **{}**.")
                    mail.story(barber_kill_story(me.id,player.id))
                    mail.spam(">kill <@{}> {} 1".format(player.id,player.emoji))
                    return mail

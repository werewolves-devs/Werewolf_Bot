from management.game import db_get, db_set
from management.general import gen_get, gen_set

next = '|            '
success = '|---> '
failure = '|'
skull = '💀 '

class Player:
    def __init__(self,user):
        self.id = user.id
        self.name = user.name
        self.bot = user.bot

        # TODO: If the user does not exist in the database yet, add them.
    


class Participant(Player):

    def __name_get(self):
        return db_get(self.id,"name")
    def __name_set(self,value):
        db_set(self.id,"name",value)
        gen_set(self.id,"name",value)

    def __emoji_get(self):
        return db_get(self.id,"emoji")
    def __emoji_set(self,value):
        db_set(self.id,"emoji",value)
    
    def __idle_get(self):
        return db_get(self.id,"activity")
    def __idle_set(self,value):
        db_set(self.id,"activity",value)

    def __channel_get(self):
        return db_get(self.id,"channel")
    def __channel_set(self,value):
        db_set(self.id,"channel",value)

    def __role_get(self):
        return db_get(self.id,"role")
    def __role_set(self,value):
        db_set(self.id,"role",value)

    def __fakerole_get(self):
        return db_get(self.id,"fakerole")
    def __fakerole_set(self,value):
        db_set(self.id,"fakerole",value)

    def __uses_get(self):
        return int(db_get(self.id,"uses"))
    def __uses_set(self,value):
        db_set(self.id,"uses",value)

    def __votes_get(self):
        return int(db_get(self.id,"votes"))
    def __votes_set(self,value):
        db_set(self.id,"votes",value)
    
    def __threatened_get(self):
        return int(db_get(self.id,"threatened"))
    def __threatened_set(self,value):
        db_set(self.id,"threatened",value)
    
    def __enchanted_get(self):
        enchanted = int(db_get(self.id,"enchanted"))
        if enchanted == 1:
            return True
        return False
    def __enchanted_set(self,value):
        if value == True:
            db_set(self.id,"enchanted",1)
        else:
            db_set(self.id,"enchanted",0)
    
    def __demonized_get(self):
        demonized = int(db_get(self.id,"demonized"))
        if demonized == 1:
            return True
        return False
    def __demonized_set(self,value):
        if value == True:
            db_set(self.id,"demonized",1)
        else:
            db_set(self.id,"demonized",0)
    
    def __powdered_get(self):
        powdered = int(db_get(self.id,"powdered"))
        if powdered == 1:
            return True
        return False
    def __powdered_set(self,value):
        if value == True:
            db_set(self.id,"powdered",1)
        else:
            db_set(self.id,"powdered",0)
    
    def __frozen_get(self):
        frozen = int(db_get(self.id,"frozen"))
        if frozen == 1:
            return True
        return False
    def __frozen_set(self,value):
        if value == True:
            db_set(self.id,"frozen",1)
        else:
            db_set(self.id,"frozen",0)
    
    def __undead_get(self):
        undead = int(db_get(self.id,"undead"))
        if undead == 1:
            return True
        return False
    def __undead_set(self,value):
        if value == True:
            db_set(self.id,"undead",1)
        else:
            db_set(self.id,"undead",0)

    def __bites_get(self):
        return int(db_get(self.id,"bites"))
    def __bites_set(self,value):
        db_set(self.id,"bites",value)
    
    def __bitten_get(self):
        bitten = int(db_get(self.id,"bitten"))
        if bitten == 1:
            return True
        return False
    def __bitten_set(self,value):
        if value == True:
            db_set(self.id,"bitten",1)
        else:
            db_set(self.id,"bitten",0)

    def __souls_get(self):
        return int(db_get(self.id,"souls"))
    def __souls_set(self,value):
        db_set(self.id,"souls",value)

    def __soulless_get(self):
        souls = int(db_get(self.id,"souls"))
        if souls >= 0:
            return True
        return False
    def __soulless_set(self,value):
        if value == True:
            db_set(self.id,"souls",0)
        else:
            db_set(self.id,"souls",-1)

    def __sleepingover_get(self):
        sleepingover = int(db_get(self.id,"sleepingover"))
        if sleepingover == 1:
            return True
        return False
    def __sleepingover_set(self,value):
        if value == True:
            db_set(self.id,"sleepingover",1)
        else:
            db_set(self.id,"sleepingover",0)

    def __protected_get(self):
        protected = int(db_get(self.id,"protected"))
        if protected == 1:
            return True
        return False
    def __protected_set(self,value):
        if value == True:
            db_set(self.id,"protected",1)
        else:
            db_set(self.id,"protected",0)

    def __abducted_get(self):
        abducted = int(db_get(self.id,"abducted"))
        if abducted == 1:
            return True
        return False
    def __abducted_set(self,value):
        if value == True:
            db_set(self.id,"abducted",1)
        else:
            db_set(self.id,"abducted",0)

    def __ccs_get(self):
        return int(db_get(self.id,"ccs"))
    def __ccs_set(self,value):
        db_set(self.id,"ccs",value)

    def __horseman_get(self):
        return int(db_get(self.id,"horseman"))
    def __horseman_set(self,value):
        db_set(self.id,"horseman",value)

    def __amulet_get(self):
        return int(db_get(self.id,"amulet"))
    def __amulet_set(self,value):
        db_set(self.id,"amulet",value)


    name = property(__name_get,__name_set)
    emoji = property(__emoji_get,__emoji_set)
    idle = property(__idle_get,__idle_set)
    channel = property(__channel_get,__channel_set)
    role = property(__role_get,__role_set)
    fakerole = property(__fakerole_get,__fakerole_set)
    uses = property(__uses_get,__uses_set)
    votes = property(__votes_get,__votes_set)
    threatened = property(__threatened_get,__threatened_set)
    enchanted = property(__enchanted_get,__enchanted_set)
    demonized = property(__demonized_get,__demonized_set)
    powdered = property(__powdered_get,__powdered_set)
    frozen = property(__frozen_get,__frozen_set)
    undead = property(__undead_get,__undead_set)
    bites = property(__bites_get,__bites_set)
    bitten = property(__bitten_get,__bitten_set)
    souls = property(__souls_get,__souls_set)
    soulless = property(__soulless_get,__soulless_set)
    sleepingover = property(__sleepingover_get,__sleepingover_set)
    protected = property(__protected_get,__protected_set)
    abducted = property(__abducted_get,__abducted_set)
    ccs = property(__ccs_get,__ccs_set)
    horseman = property(__horseman_get,__horseman_set)
    amulet = property(__amulet_get,__amulet_set)
from management.game import db_get, db_set

class Player:
    def __init__(self,user):
        self.id = user.id
        self.name = user.name
        self.bot = user.bot

    def __name_get(self):
        return db_get(self.id,"name")
    def __name_set(self,value):
        db_set(self.id,"name",value)

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
        return db_get(self.id,"uses")
    def __uses_set(self,value):
        db_set(self.id,"uses",value)

    def __votes_get(self):
        return db_get(self.id,"votes")
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

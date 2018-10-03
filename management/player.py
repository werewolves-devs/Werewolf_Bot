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

    name = property(__name_get,__name_set)
    emoji = property(__emoji_get,__emoji_set)
    idle = property(__idle_get,__idle_set)
    channel = property(__channel_get,__channel_set)


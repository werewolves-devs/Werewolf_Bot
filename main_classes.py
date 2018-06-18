from config import game_log

# This class is being used to pass on to above. While the administration is done underneath the hood, messages are passed out to give the Game Masters and the players an idea what has happened.
class Mailbox:
    def __init__(self):
        self.gamelog = []       # Send message to gamelog channel
        self.botspam = []       # Send message to botspam channel
        self.storytime = []     # Send message to storytime channel
        self.channel = []       # Send message to channel
        self.player = []        # Send message to user
        self.newchannels = []   # Create new channel
        self.oldchannels = []   # Edit existing channel

    def log(self,content,temporary = False):
        """Send a message to the gamelog channel"""
        self.gamelog.append(Message(content,temporary))
        return self
    def log_add(self,moar_content):
        """Add some text to the last gamelog message"""
        self.gamelog[-1].add(moar_content)
        return self

    def spam(self,content,temporary = False):
        """Send a message to the botspam channel"""
        self.botspam.append(Message(content,temporary))
        return self
    def spam_add(self,moar_content):
        """Add some text to the last botspam message"""
        self.botspam[-1].add(moar_content)
        return self

    def story(self,content,temporary = False):
        """Send a message to the storytime channel"""
        self.storytime.append(Message(content,temporary))
        return self
    def story_add(self,moar_content):
        """Add some text to the last storytime message"""
        self.storytime[-1].add(moar_content)
        return self

    def msg(self,content,destination,temporary = False):
        """Send a message to a given channel"""
        self.channel.append(Message(content,temporary,destination))
        return self
    def msg_add(self,moar_content):
        """Add some text to the last message"""
        self.channel[-1].add(moar_content)
        return self

    def dm(self,content,user_id,temporary = False):
        """Send a DM to a given user"""
        self.player.append(Message(content,temporary,user_id))
        return self
    def dm_add(self,moar_content):
        """Add some text to the last DM"""
        self.player[-1].add(moar_content)
        return self
  
    def create_cc(self,channel_name,channel_owner,settlers=[]):
        """Send an order to create a channel"""
        self.newchannels.append(ChannelCreate(channel_name,channel_owner,settlers))
        return self
    def edit_cc(self,channel_id,user_id,number):
        """Send an order to edit a channel"""
        self.oldchannels.append(ChannelChange(channel_id,user_id,number))
        return self

# Class used to send messages through the mailbox
class Message:
    def __init__(self,content,temporary = False,destination = ''):
        self.content = content
        self.temporary = temporary
        self.destination = destination
    def add(self,moar_content):
        self.content += str(moar_content)
        return self

# Class for sending commands back to main.py to create/alter channels
class ChannelCreate:
    def __init__(self,name,owner,settlers=[]):
        self.name = name
        self.owner = owner
        self.settlers = []
        
class ChannelChange:
    def __init__(self,channel,victim,number):
        self.channel = channel
        self.victim = victim
        self.number = number

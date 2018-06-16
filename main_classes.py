import roles
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
        self.gamelog.append(Message(content,temporary))
    def log_add(self,moar_content):
        self.gamelog[-1].add(moar_content)
    
    def spam(self,content,temporary = False):
        self.botspam.append(Message(content,temporary))
    def spam_add(self,moar_content):
        self.botspam[-1].add(moar_content)

    def story(self,content,temporary = False):
        self.storytime.append(Message(content,temporary))
    def story_add(self,moar_content):
        self.storytime[-1].add(moar_content)
    
    def msg(self,content,destination,temporary = False):
        self.channel.append(Message(content,temporary,destination))
    def msg_add(self,moar_content):
        self.channel[-1].add(moar_content)
    
    def dm(self,content,user_id,temporary = False):
        self.player.append(Message(content,temporary,user_id))
    def dm_add(self,moar_content):
        self.player[-1].add(moar_content)
    
    def create_cc(self,channel_name,channel_owner,settlers=[]):
        self.newchannels.append(ChannelComm(0,channel_name,channel_owner,'',0,settlers))
    def edit_cc(self,channel_id,user_id,number):
        self.oldchannels.append(ChannelComm(channel_id,'','',user_id,number))

# Class used to send messages through the mailbox
class Message:
    def __init__(self,content,temporary = False,destination = ''):
        self.content = content
        self.temporary = temporary
        self.destination = destination
    
    def add(self,moar_content):
        self.content += str(moar_content)

# Class for sending commands back to main.py to create/alter channels
class ChannelComm:
    def __init__(self,channel_id,channel_name,channel_owner,victim = '',number = 0,settlers=[]):
        # If channel_id == 0, then it should create a new channel
        self.channel = channel_id
        self.name = channel_name
        self.victim = victim
        self.number = number
        self.owner = channel_owner
        self.settlers = []
        

from config import game_log

# This class is being used to pass on to above. While the administration is done underneath the hood, messages are passed out to give the Game Masters and the players an idea what has happened.
class Mailbox:
    def __init__(self,evaluate_polls = False):
        self.gamelog = []       # Send message to gamelog channel
        self.botspam = []       # Send message to botspam channel
        self.storytime = []     # Send message to storytime channel
        self.answer = []        # Send message to triggered channel
        self.channel = []       # Send message to channel
        self.player = []        # Send message to user
        self.newchannels = []   # Create new channel
        self.oldchannels = []   # Edit existing channel
        self.polls = []         # Create new polls

        self.evaluate_polls = evaluate_polls

    def log(self,content,temporary = False,reactions = []):
        """Send a message to the gamelog channel."""
        self.gamelog.append(Message(content,temporary,'',reactions))
        return self
    def log_add(self,moar_content):
        """Add some text to the last gamelog message"""
        self.gamelog[-1].add(moar_content)
        return self
    def log_react(self,emoji):
        """Add a reaction to the last gamelog message"""
        self.gamelog[-1].react(emoji)
        return self

    def spam(self,content,temporary = False,reactions = []):
        """Send a message to the botspam channel"""
        self.botspam.append(Message(content,temporary,'',reactions))
        return self
    def spam_add(self,moar_content):
        """Add some text to the last botspam message"""
        self.botspam[-1].add(moar_content)
        return self
    def spam_react(self,emoji):
        """Add a reaction to the last botspam message"""
        self.botspam[-1].react(emoji)
        return self

    def story(self,content,temporary = False,reactions = []):
        """Send a message to the storytime channel"""
        self.storytime.append(Message(content,temporary,'',reactions))
        return self
    def story_add(self,moar_content):
        """Add some text to the last storytime message"""
        self.storytime[-1].add(moar_content)
        return self
    def story_react(self,emoji):
        """Add a reaction to the last storytime message"""
        self.storytime[-1].react(emoji)
        return self

    def respond(self,content,temporary = False,reactions = []):
        """Send a message in the channel where a user has triggered this function."""
        self.answer.append(Message(content,temporary,'',reactions))
        return self
    def respond_add(self,moar_content):
        """Add some text to the channel that triggered the function."""
        self.answer[-1].add(moar_content)
    def respond_react(self,emoji):
        """Add a reaction to the last message to the channel that triggered the function."""
        self.answer[-1].react(emoji)
        return self

    def msg(self,content,destination,temporary = False,reactions = []):
        """Send a message to a given channel"""
        self.channel.append(Message(content,temporary,destination,reactions))
        return self
    def msg_add(self,moar_content):
        """Add some text to the last message"""
        self.channel[-1].add(moar_content)
        return self
    def msg_react(self,emoji):
        """Add a reaction to the last message"""
        self.channel[-1].react(emoji)
        return self

    def embed(self, embed, destination, temporary = False, reactions=[]):
        """Send a message to a given channel"""
        self.channel.append(Message(embed,temporary,destination,reactions,True))
        return self

    def dm(self,content,user_id,temporary = False,reactions = []):
        """Send a DM to a given user"""
        self.player.append(Message(content,temporary,user_id,reactions))
        return self
    def dm_add(self,moar_content):
        """Add some text to the last DM"""
        self.player[-1].add(moar_content)
        return self
    def dm_react(self,emoji):
        """Add a reaction to the last DM"""
        self.player[-1].react(emoji)
        return self

    def create_cc(self,channel_name,channel_owner,members = [],settlers=[]):
        """Send an order to create a channel"""
        self.newchannels.append(ChannelCreate(channel_name,channel_owner,members,settlers))
        return self
    def edit_cc(self,channel_id,user_id,number):
        """Send an order to edit a channel"""
        self.oldchannels.append(ChannelChange(channel_id,user_id,number))
        return self

    def new_poll(self,channel_id,purpose,user_id = 0,description = ''):
        """Send a request to make a poll in the given channel"""
        self.polls.append(PollRequest(channel_id,purpose,user_id,description))
        return self

# Class used to send messages through the mailbox
class Message:
    def __init__(self,content,temporary = False,destination = '',reactions=[],embed = False):
        self.content = content
        self.temporary = temporary
        self.destination = destination
        self.reactions = reactions
        self.embed = embed
    def add(self,moar_content):
        self.content += str(moar_content)
        return self
    def react(self,emoji):
        self.reactions.append(emoji)
        return self

# Class for sending commands back to main.py to create/alter channels
class ChannelCreate:
    def __init__(self,name,owner,members=[],settlers=[]):
        self.name = name
        self.owner = owner
        self.members = members
        self.settlers = settlers
        if owner not in members:
            self.members.append((owner))

class ChannelChange:
    # Notice how settlers is not a value here, while it does happen in games that a user switches standard channels.
    # This is because settlers is just a database function to execute. When changing a channel, the id is known and
    # can be executed easily. However, this isn't the case when the channel doesn't yet exist.
    def __init__(self,channel,victim,number):
        self.channel = channel
        self.victim = victim
        self.number = number

class PollRequest:
    def __init__(self,channel_id,purpose,user_id,description):
        self.channel = channel_id
        self.purpose = purpose
        self.user_id = user_id

        if len(description) > 512:
            self.description = description[0:512]
        else:
            self.description = description

class PollToEvaluate:
    def __init__(self,database_tuple):
        self.msg_table = database_tuple[1]
        self.blamed = database_tuple[2]

        self.msg_table = [int(database_tuple[i+3]) for i in range(len(database_tuple) - 3) if int(database_tuple[i+3]) != 0]

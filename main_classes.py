from management.db import db_get, db_set, channel_change_all, channel_get, get_secret_channels
from config import game_log, shop_file

# This class is being used to pass on to above. While the administration is done underneath the hood, messages are passed out to give the Game Masters and the players an idea what has happened.
class Mailbox:
    def __init__(self,evaluate_polls = False):
        self.gamelog = []          # Send message to gamelog channel
        self.botspam = []          # Send message to botspam channel
        self.storytime = []        # Send message to storytime channel
        self.answer = []           # Send message to triggered channel
        self.channel = []          # Send message to channel
        self.player = []           # Send message to user
        self.newchannels = []      # Create new channel
        self.oldchannels = []      # Edit existing channel
        self.polls = []            # Create new polls
        self.deletecategories = [] # Delete categories and channels they contain
        self.demotions = []        # Remove Mayor + Reporter role
        self.shops = []            # Create shop
        self.cleaners = []         # Delete all trash messages from given channel

        self.evaluate_polls = evaluate_polls

    # ------------------------------
    # Commands for easier management
    # ------------------------------
    def __len__(self):
        length = len(self.gamelog) + len(self.botspam) + len(self.storytime) + len(self.answer)
        length += len(self.channel) + len(self.player) + len(self.newchannels) + len(self.oldchannels)
        length += len(self.polls) + len(self.deletecategories) + len(self.demotions) + len(self.shops)
        length += len(self.cleaners)
        return length
    
    def __repr__(self):
        answer = "<MAILBOX|"
        if self.gamelog != []:          answer += "|gamelog={}".format(self.gamelog)
        if self.botspam != []:          answer += "|botspam={}".format(self.botspam)
        if self.storytime != []:        answer += "|story={}".format(self.storytime)
        if self.answer != []:           answer += "|answer={}".format(self.answer)
        if self.channel != []:          answer += "|channel={}".format(self.channel)
        if self.player != []:           answer += "|player={}".format(self.player)
        if self.newchannels != []:      answer += "|newchannels={}".format(self.newchannels)
        if self.oldchannels != []:      answer += "|oldchannels={}".format(self.oldchannels)
        if self.polls != []:            answer += "|polls={}".format(self.polls)
        if self.deletecategories != []: answer += "|deletecategories={}".format(self.deletecategories)
        if self.demotions != []:        answer += "|demotions={}".format(self.demotions)
        if self.shops != []:            answer += "|shops={}".format(self.shops)
        if self.cleaners != []:         answer += "|cleaners={}".format(self.cleaners)
        answer += "|"
        answer += "|evaluate_polls={}".format(self.evaluate_polls)
        answer += ">"
        return answer

    # ------------------------------

    def log(self,content,temporary = False,reactions = []):
        """Send a message to the gamelog channel."""
        self.gamelog.append(Message(content,temporary,'',reactions))
        return self
    def log_add(self,moar_content):
        """Add some text to the last gamelog message"""
        if len(self.gamelog[-1].content) + len(moar_content) > 1950:
            self.log(moar_content,self.gamelog[-1].temporary)
            return self
            
        self.gamelog[-1].add(moar_content)
        return self
    def log_react(self,emoji):
        """Add a reaction to the last gamelog message"""
        self.gamelog[-1].react(emoji)
        return self

    def shop(self, destination, shop_config = ''):
        """Add a shop"""
        self.shops.append(Shop(destination, shop_config))
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
        last_msg = self.channel[-1]

        if len(last_msg.content) + len(moar_content) > 1950:
            self.msg(moar_content,last_msg.destination)
            return self

        last_msg.add(moar_content)
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

    def create_cc(self,channel_name,channel_owner,members = [],settlers=[],secret=False,trashy=False):
        """Send an order to create a channel"""
        self.newchannels.append(ChannelCreate(channel_name,channel_owner,members,settlers,secret,trashy))
        return self
    def edit_cc(self,channel_id,user_id,number):
        """Send an order to edit a channel"""
        self.oldchannels.append(ChannelChange(channel_id,user_id,number))
        return self
        
    def create_sc(self,user_id,role):
        """Create a new secret channel for a given user."""
        new_role = ''
        for i in range(len(role)):
            if role[i] == ' ':
                new_role += '_'
            else:
                new_role += role[i]
        self.create_cc(new_role,0,[user_id],[user_id],True)
        return self
    def add_to_sc(self,user_id,role):
        """Add a user to a yet to be made secret channel."""
        new_role = ''
        for i in range(len(role)):
            if role[i] == ' ':
                new_role += '_'
            else:
                new_role += role[i]
        for channel in self.newchannels:
            if channel.secret and channel.name == new_role:
                if user_id not in channel.members:
                    channel.members.append(user_id)
                if user_id not in channel.settlers:
                    channel.settlers.append(user_id)
                return self
        self.create_sc(user_id,new_role)
        return self

    def new_poll(self,channel_id,purpose,user_id = 0,description = ''):
        """Send a request to make a poll in the given channel"""
        self.polls.append(PollRequest(channel_id,purpose,user_id,description))
        return self

    def delete_category(self, channel_id):
        self.deletecategories.append(CategoryDelete(channel_id))
        return self

    def cleanup(self,channel_id):
        """Add a channel that needs to be erased from content."""
        self.cleaners.append(channel_id)
        return self
    
    # Commands that change one's cc status
    def freeze(self,user_id):
        """Freeze a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
        db_set(user_id,'frozen',1)
        self.spam("<@{}> was frozen.".format(user_id))
        to_freeze = channel_change_all(user_id,1,2)

        for channel_id in get_secret_channels('Frozen_Realm'):
            self.edit_cc(channel_id,user_id,1)
        for channel_id in to_freeze:
            self.edit_cc(channel_id,user_id,2)
        return self
    
    def unfreeze(self,user_id):
        """Unfreeze a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
        db_set(user_id,'frozen',0)
        self.spam("<@{}> is no longer frozen.".format(user_id))

        to_unfreeze = channel_change_all(user_id,2,1)

        for channel_id in get_secret_channels('Frozen_Realm'):
            self.edit_cc(channel_id,user_id,0)
        for channel_id in to_unfreeze:
            self.edit_cc(channel_id,user_id,1)
        return self
    
    def abduct(self,user_id):
        """Abduct a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
        db_set(user_id,'abducted',1)
        self.spam("<@{}> has been abducted.".format(user_id))

        for channel_id in channel_change_all(user_id,1,3):
            self.edit_cc(channel_id,user_id,3)
        for channel_id in channel_change_all(user_id,5,6):
            self.edit_cc(channel_id,user_id,6)
        for channel_id in get_secret_channels('Swamp'):
            self.edit_cc(channel_id,user_id,1)
        return self
    
    def unabduct(self,user_id):
        """Unabduct a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
        db_set(user_id,'abducted',0)
        self.spam("<@{}> is no longer abducted.".format(user_id))
    
        for channel_id in channel_change_all(user_id,3,1):
            self.edit_cc(channel_id,user_id,1)
        for channel_id in channel_change_all(user_id,6,5):
            self.edit_cc(channel_id,user_id,5)
        for channel_id in channel_change_all(user_id,7,4):
            self.edit_cc(channel_id,user_id,4)
        return self
    
    def suspend(self,user_id):
        """Suspend a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
        db_set(user_id,'role','Suspended')
        self.spam("<@{}> has been suspended.".format(user_id))

        for channel_id in channel_change_all(user_id,1,8):
            self.edit_cc(channel_id,user_id,8)
        for channel_id in channel_change_all(user_id,2,8):
            self.edit_cc(channel_id,user_id,8)
        for channel_id in channel_change_all(user_id,3,8):
            self.edit_cc(channel_id,user_id,8)
        for channel_id in channel_change_all(user_id,4,8):
            self.edit_cc(channel_id,user_id,8)
        for channel_id in channel_change_all(user_id,5,8):
            self.edit_cc(channel_id,user_id,8)
        for channel_id in channel_change_all(user_id,6,8):
            self.edit_cc(channel_id,user_id,8)
        for channel_id in channel_change_all(user_id,7,8):
            self.edit_cc(channel_id,user_id,8) 
        return self     

    def mute(self,user_id,channel_id):
        """Mute a user. Users cannot be muted in channels they do not take part in, or channels they are frozen in.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
        self.spam("<@{}> has been muted in <#{}>".format(user_id,channel_id))

        channel_settings = int(channel_get(channel_id,user_id))

        if channel_settings == 1:
            self.edit_cc(channel_id,user_id,5)
        if channel_settings == 3:
            self.edit_cc(channel_id,user_id,6)
        return self
    
    def remove_proms(self,user_id):
        """Remove the Mayor and Reporter role from the given user.  
        
        Keyword arguments:  
        user_id -> the user who must lose the roles"""
        self.demotions.append(int(user_id))


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
    def __repr__(self):
        temp_content = self.content[0:min(20,len(self.content))]
        if len(self.content) > 20:
            temp_content += '...'
        answer = "<Message|"
        if temp_content != "":      answer += "|content=\'{}\'".format(temp_content)
        if self.destination != "":  answer += "|destination={}".format(self.destination)
        if self.reactions != []:    answer += "|reactions={}".format(self.reactions)
        answer += "|"
        if self.temporary != False: answer += "|temporary={}".format(self.temporary)
        if self.embed != False:     answer += "|embed={}".format(self.embed)
        answer += ">"
        return answer

# Class for creating a shop embed
class Shop:
    def __init__(self, destination, shop_config = shop_file):
        self.destination = destination
        self.shop_config = shop_config
    def __repr__(self):
        answer = "<Shop|"
        answer += "|destination={}".format(self.destination)
        if self.shop_config != shop_file:   answer += "|shop_config={}".format(self.shop_config)
        answer += ">"
        return answer

# Class for sending commands back to main.py to create/alter channels
class ChannelCreate:
    def __init__(self,name,owner,members=[],settlers=[],secret=False,trashy=False):
        self.name = name
        self.owner = owner
        self.members = members
        self.settlers = settlers
        self.secret = secret
        self.trashy = trashy
        if owner not in members and owner != 0:
            self.members.append((owner))

    def __repr__(self):
        answer = "<ChannelCreate|"
        answer += "|name={}".format(self.name)
        answer += "|owner={}".format(self.owner)
        if self.members != []:  answer += "|members={}".format(self.members)
        if self.settlers != []: answer += "|settlers={}".format(self.settlers)
        answer += "|"
        if self.secret == True: answer += "|secret={}".format(self.secret)
        if self.trashy == True: answer += "|trashy={}".format(self.trashy)
        answer += ">"
        return answer

class ChannelChange:
    # Notice how settlers is not a value here, while it does happen in games that a user switches standard channels.
    # This is because settlers is just a database function to execute. When changing a channel, the id is known and
    # can be executed easily. However, this isn't the case when the channel doesn't yet exist.
    def __init__(self,channel,victim,number):
        self.channel = channel
        self.victim = victim
        self.number = number

    def __repr__(self):
        return "<ChannelChange||channel={}|victim={}|number={}>".format(self.channel,self.victim,self.number)

class CategoryDelete:
    # Notice how settlers is not a value here, while it does happen in games that a user switches standard channels.
    # This is because settlers is just a database function to execute. When changing a channel, the id is known and
    # can be executed easily. However, this isn't the case when the channel doesn't yet exist.
    def __init__(self,channel):
        self.channel = channel

    def __repr__(self):
        return "<CategoryDelete||channel={}>".format(self.channel)
    

class PollRequest:
    def __init__(self,channel_id,purpose,user_id,description):
        self.channel = channel_id
        self.purpose = purpose
        self.user_id = user_id

        if len(description) > 512:
            self.description = description[0:512]
        else:
            self.description = description
    
    def __repr__(self):
        temp_desc = self.description[0:min(20,len(self.description))]
        if len(self.description) > 20:
            temp_desc += '...'
        return "<PollRequest||channel={}|purpose={}|user={}|desc=\'{}\'>".format(self.channel,self.purpose,self.user_id,temp_desc)
    

class PollToEvaluate:
    def __init__(self,database_tuple):
        self.purpose = database_tuple[1]
        self.blamed = database_tuple[2]
        self.channel = database_tuple[3]

        self.msg_table = [int(database_tuple[i+4]) for i in range(len(database_tuple) - 4) if int(database_tuple[i+4]) != 0]
    
    def __repr__(self):
        return "<PollToEvaluate||purpose={}|blamed=\'{}\'|channel={}|msg_table={}>".format(self.purpose,self.blamed,self.channel,self.msg_table)

if __name__ == "__main__":
    print(PollToEvaluate(['lynch','','12345','1','2','3']))
    print("{}".format(PollToEvaluate(['lynch','','12345','1','2','3'])))
    print(str(PollToEvaluate(['lynch','','12345','1','2','3'])))

    print(PollRequest(100,'Mayor',1234,"It was a hairy night in Tumble Town. Oh, btw, we need a Mayor."))

    answer = Mailbox().log("Hi there!")
    answer.log("This is a test!\n")
    answer.log_add("Woohoo!")
    answer.edit_cc(123124312,123423523,3)
    print(answer)
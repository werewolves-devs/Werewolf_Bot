from config import Destination

class Mailbox:
    def __init__(self,evaluate_polls = False):
        self.messages = []
        self.answers = []
        self.dms = []

        self.evaluate_polls = evaluate_polls

    # ------------------------------
    # Commands for easier management
    # ------------------------------
    def __len__(self):
        return 0 # TODO
    
    def __repr__(self):
        return '<TODO>'

    # ------------------------------

    def __select_channel(self,destination):
        return [message for message in self.messages if message.destination == destination]

    def msg(self,content,destination,temporary=False,reactions=[],embed=False):
        self.messages.append(Message(content,destination,temporary,reactions,embed))
        return self
    def msg_add(self,moar_content,message_list=None):
        if message_list == None:
            message_list = self.messages

        last = message_list[-1]
        if len(last) + len(moar_content) > 1950:
            self.msg(moar_content,last.destination,last.temporary,last.reactions,last.embed)
        else:
            last.add(moar_content)
        return self
    def msg_react(self,emoji,message_list=None):
        if message_list == None:
            message_list = self.messages

        last = message_list[-1]
        last.react(emoji)
        return self

    def log(self,content,temporary = False,reactions = [],embed=False):
        return self.msg(content,Destination.game_log,temporary,reactions,embed)
    def log_add(self,moar_content):
        return self.msg_add(moar_content,self.__select_channel(Destination.game_log))
    def log_react(self,emoji):
        return self.msg_react(emoji,self.__select_channel(Destination.game_log))

    def shop(self, destination, shop_config = ''):
        """Add a shop"""

    def spam(self,content,temporary = False,reactions = [],embed=False):
        return self.msg(content,Destination.bot_spam,temporary,reactions,embed)
    def spam_add(self,moar_content):
        return self.msg_add(moar_content,self.__select_channel(Destination.bot_spam))
    def spam_react(self,emoji):
        return self.msg_react(emoji,self.__select_channel(Destination.bot_spam))

    def story(self,content,temporary = False,reactions = [],embed=False):
        return self.msg(content,Destination.story_time,temporary,reactions,embed)
    def story_add(self,moar_content):
        return self.msg_add(moar_content,self.__select_channel(Destination.story_time))
    def story_react(self,emoji):
        return self.msg_react(emoji,self.__select_channel(Destination.story_time))

    def respond(self,content,temporary = False,reactions = [],embed=False):
        self.answers.append(Message(content,0,temporary,reactions,embed))
        return self
    def respond_add(self,moar_content):
        return self.msg_add(moar_content,self.answers)
    def respond_react(self,emoji):
        return self.msg_react(emoji,self.answers)

    def dm(self,content,user_id,temporary = False,reactions = [],embed=False):
        self.dms.append(Message(content,0,temporary,reactions,embed))
        return self
    def dm_add(self,moar_content):
        return self.msg_add(moar_content,self.dms)
    def dm_react(self,emoji):
        return self.msg_react(emoji,self.dms)

    def create_cc(self,channel_name,channel_owner,members = [],settlers=[],secret=False,trashy=False):
        """Send an order to create a channel"""
    def edit_cc(self,channel_id,user_id,number):
        """Send an order to edit a channel"""
        
    def create_sc(self,user_id,role):
        """Create a new secret channel for a given user."""
    def add_to_sc(self,user_id,role):
        """Add a user to a yet to be made secret channel."""

    def new_poll(self,channel_id,purpose,user_id = 0,description = ''):
        """Send a request to make a poll in the given channel"""

    def delete_category(self, channel_id):
        self.deletecategories.append(CategoryDelete(channel_id))
        return self

    def cleanup(self,channel_id):
        """Add a channel that needs to be erased from content."""
    
    def thank(self,message):
        """Add a message that needs to be erased."""
    
    def gift(self,user_id):
        """Add a user that is given a gift."""

    # Commands that change one's cc status
    def freeze(self,user_id):
        """Freeze a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
    
    def unfreeze(self,user_id):
        """Unfreeze a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
    
    def abduct(self,user_id):
        """Abduct a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
    
    def unabduct(self,user_id):
        """Unabduct a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
    
    def suspend(self,user_id):
        """Suspend a user.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""  

    def mute(self,user_id,channel_id):
        """Mute a user. Users cannot be muted in channels they do not take part in, or channels they are frozen in.  
        This function alters the Mailbox, so 'add' and react commands may not work as intended."""
    
    def remove_proms(self,user_id):
        """Remove the Mayor and Reporter role from the given user.  
        
        Keyword arguments:  
        user_id -> the user who must lose the roles"""

# Class used to send messages through the mailbox
class Message:
    def __init__(self,content,destination,temporary = False,reactions=[],embed = False):
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

    def __len__(self):
        return len(self.content)

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
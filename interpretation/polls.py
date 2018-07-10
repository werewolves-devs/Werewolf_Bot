from management.db import db_get, player_list

class Vote:
    def __init__(self,user_id, emoji, purpose):
        self.user = user_id
        self.emoji = emoji
        self.votes = 1
        if int(db_get(user_id,'undead')) == 1:
            self.votes = 0
        if purpose == 'lynch':
            self.votes = db_get(user_id,'votes')

class Disqualified:
    def __init__(self,user_id,reason = 0):
        self.user = user_id

        self.reason = reason
        # 0 - double voting
        # 1 - self voting

def count_votes(voting_table, purpose = 'lynch'):
    user_table = []
    blacklist = []
    emoji_table = []

    for vote in voting_table:
        # Add new emoji
        if vote[1] not in emoji_table:
            emoji_table.append(vote[1])
        
        # Raise alarm if user already voted
        if vote[0] in blacklist:
            pass
        elif vote[0] in user_table:
            blacklist.append(vote[0])
            user_table.remove(vote[0])
        else:
            user_table.append(vote[0])
    
    # Evaluate table, filter double votes and continue
    voting_table = [Vote(vote[0],vote[1],purpose) for vote in user_table if vote[0] in user_table]
    blacklist = [Disqualified(user) for user in blacklist]

    if purpose == 'lynch':
        for user in player_list():
            if int(db_get(user,'threatened')) > 0:
                voting_table.append(Vote(0,db_get(user,'emoji'),"**RAVEN THREAT**"))

    # Create the evaluation messages
    answer = "**__Poll results:__**\n\n"
    log = "**__Poll results:__**\n\n"

    for emoji in emoji_table:
        emoji_votes = [vote for vote in voting_table if vote.emoji == emoji]



        

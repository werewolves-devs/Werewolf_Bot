def db_get(user_id,bla):
    return -10
def player_list():
    return []
def emoji_to_player(emoji):
    return -4

class Vote:
    def __init__(self,user_id, emoji, purpose, reason = ''):
        self.user = user_id
        self.emoji = emoji
        self.votes = 1
        self.reason = reason
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

def count_votes(voting_table, purpose = 'lynch', mayor = 0):
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
    voting_table = [Vote(vote[0],vote[1],purpose) for vote in voting_table if vote[0] in user_table]
    voting_table.append(Vote(0,':smirk:',2,"**RAVEN THREAT**"))
    blacklist = [Disqualified(user) for user in blacklist]

    if purpose == 'lynch':
        for user in player_list():
            if int(db_get(user,'threatened')) > 0:
                voting_table.append(Vote(0,db_get(user,'emoji'),2,"**RAVEN THREAT**"))

    # Create the evaluation messages
    answer = "**__Poll results:__**\n\n"
    log = "**__Poll results:__**\n\n"
    max_i = 0
    chosen_emoji = ''

    for emoji in emoji_table:
        emoji_votes = [vote for vote in voting_table if vote.emoji == emoji]

        if emoji_votes != []:
            answer += "{}\n".format(emoji)
            log += "{}\n".format(emoji)
        i = 0

        for vote in emoji_votes:
            if vote.user == emoji_to_player(emoji) and purpose not in ["Mayor","Reporter"]:
                blacklist.append(Disqualified(vote.user,1))
            elif vote.user == 0 and vote.votes > 0:
                log += vote.reason
                if vote.votes > 1:
                    log += " *({}x)*".format(vote.votes)
                log += '\n'

                i += vote.votes
            else:
                answer += "<@{}> ".format(vote.user)
                log += "<@{}> ".format(vote.user)
                if vote.user == mayor:
                    vote.votes += 1
                    answer += "- @Mayor"
                    log += "- @Mayor"
                if vote.votes > 1:
                    log += " *({}x)*".format(vote.votes)
                i += vote.votes
                log += '\n'
                answer += '\n'
        
        if i > 0:
            log += "**TOTAL: {} votes**\n\n".format(i)
    
        if i == max_i:
            chosen_emoji = ''
        if i > max_i:
            chosen_emoji = emoji
            max_i = i
    
    for cheater in blacklist:
        if cheater.reason == 0:
            answer += "<@{}>, you have been disqualified for double voting.\n".format(cheater.user)
        if cheater.reason == 1:
            answer += "<@{}>, your vote has been disqualified for you may not vote for yourself on this poll.".format(cheater.user)
    
    return log, answer, chosen_emoji

if __name__ == "__main__":
    log, answer, chosen_emoji = count_votes([[1,':smirk:'],[2,':smirk:'],[3,':smirk:'],[4,':grin:'],[5,':smirk:'],[3,':grin:'],[8,':grin:']],'wolf',8)
    print(log)
    print(chosen_emoji)
    print(answer)

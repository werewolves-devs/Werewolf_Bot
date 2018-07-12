from management.db import db_get, emoji_to_player, player_list, isParticipant
from management.dynamic import day_number

class Vote:
    def __init__(self,user_id, emoji, purpose, reason = ''):
        self.user = user_id
        self.emoji = emoji
        self.votes = 1
        self.reason = reason
        if reason == "**RAVEN THREAT**":
            self.votes == int(db_get(purpose,'threatened'))
            print(self.votes)
        else:
            if int(db_get(user_id,'undead')) == 1:
                self.votes = 0
            if purpose in ['lynch','Mayor','Reporter']:
                self.votes = db_get(user_id,'votes')

class Disqualified:
    def __init__(self,user_id,reason = 0):
        self.user = user_id

        self.reason = reason
        # 0 - double voting
        # 1 - self voting

def count_votes(voting_table, purpose = 'lynch', mayor = 0):
    """Count votes based on reactions given to """
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
    blacklist = [Disqualified(user) for user in blacklist]

    if purpose == 'lynch':
        for user in player_list():
            if int(db_get(user,'threatened')) > 0:
                voting_table.append(Vote(0,db_get(user,'emoji'),user,"**RAVEN THREAT**"))

    print([[vote.user,vote.emoji,vote.votes] for vote in voting_table])

    # Create the evaluation messages
    answer = "**__Poll results "
    log = "**__Poll results "

    if purpose == 'wolf':
        answer += "from wolf attack:__**\n"
        log += "from wolf attack:__**\n"
    elif purpose == 'cult':
        answer += "from cult attack:__**\n"
        log += "from cult attack:__**\n"
    elif purpose == 'thing':
        answer += "from the swamp:__**\n"
        log += "from the swamp:__**\n"
    elif purpose == 'lynch':
        answer += "from public execution on day {}:__**\n".format(day_number())
        log += "from public execution on day {}:__**\n".format(day_number())
    elif purpose == 'Mayor':
        answer += "from Mayor election:__**\n"
        log += "from Mayor election:__**\n"
    elif purpose == 'Reporter':
        answer += "from Reporter election:__**\n"
        log += "from Reporter election:__**\n"


    max_i = 0
    chosen_emoji = ''

    for emoji in emoji_table:
        emoji_votes = [vote for vote in voting_table if vote.emoji == emoji]

        if emoji_votes != []:
            answer += "{} - VOTES FOR <@{}>\n".format(emoji,emoji_to_player(emoji))
            log += "{} - VOTES FOR <@{}>\n".format(emoji,emoji_to_player(emoji))
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

    answer += "\n"
    log += "\n"

    for cheater in blacklist:
        if cheater.reason == 0:
            answer += "<@{}>, you have been disqualified for double voting.\n".format(cheater.user)
            log += "<@{}> has been disqualified for double voting.\n".format(cheater.user)
        if cheater.reason == 1:
            answer += "<@{}>, your vote has been disqualified for you may not vote for yourself on this poll.\n".format(cheater.user)
            log += "<@{}> has been disqualified for voting on themselves.\n".format(cheater.user)

    if chosen_emoji != '':
        answer += "\n__The emoji {} has the most votes, making <@{}> the winner of this poll!__".format(chosen_emoji,emoji_to_player(emoji))
        log += "\n__The emoji {} has the most votes, effectively making <@{}> the winner of this poll.__".format(chosen_emoji,emoji_to_player(chosen_emoji))
    elif emoji_table != []:
        answer += "\n__It seems like we\'ve reached a tie! No-one will win this poll, I\'m sorry!__"
        log += "\n__The poll has reached a tie and will not choose a winner.__"
    else:
        answer += "\n__It seems like no-one has voted! Well, in that case, there won\'t be a winner either.__"
        log += "\n__No votes have been registered.__"

    return log, answer, chosen_emoji

from management.position import villager_team, wolf_team
from management.dynamic import get_mayor
import management.db as db

def viliager_victory():
    """This function returns true if the town's win condition has been met."""
    for user in db.player_list():
        if db.isParticipant(user) and user not in villager_team:
            return False
    return True

def wolf_victory():
    """This function returns true if the wolves' win condition has been met."""
    for user in db.player_list():
        if db.isParticipant(user) and user not in wolf_team:
            return False
    return True

def white_wolf_victory():
    """This function returns true if the white werewolf has won."""
    winner = 0
    for user in db.player_list():
        if db.isParticipant(user):
            if winner > 0:
                return False
            if db.db_get(user,'role') != 'White Werewolf':
                return False
            winner += 1
    return True

def flute_victory():
    """This function returns true if the flute players have won."""
    for user in db.player_list():
        if db.isParticipant(user):
            if db.db_get(user,'role') != 'Flute Player' and db.db_get(user,'enchanted') == 0:
                return False
    return True

def despot_victory():
    if db.db_get(int(get_mayor()),'role') == 'Despot':
        return True
    return False

def devil_victory():
    for user in db.player_list():
        if db.isParticipant(user) and db.db_get(user,'role') not in ['Devil','Demon']:
            if db.db_get(user,'souls') < 0:
                return False
    return True

def ice_victory():
    """This function returns true if the ice kings have won."""
    for user in db.player_list():
        if db.isParticipant(user) and db.db_get(user,'frozen') == 0 and db.db_get(user,'role') != 'Ice King':
            return False
    return True

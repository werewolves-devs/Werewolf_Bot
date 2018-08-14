# This file contains the explanation message whenever a player switches a role DURING  THE GAME.
from management.db import db_get

def undead_change(victim_id,old_role,new_role):
    return 'You are now pretending to be innocent. You are still undead.'

def to_innocent(victim_id,old_role = 'Cursed Civlian'):
    if int(db_get(victim_id,'undead')) == 1:
        return undead_change(victim_id,old_role,'Innocent')

    msg = 'You have known your whole life that you had a curse hanging around you. You woke up with it, '
    msg += 'you worked with it, you ate with it and you went to sleep with it.\n'
    msg += 'However, you had a strange feeling lately. Not the strange way the curse gave you, no, more like an... '
    msg += 'enlighting feeling. You have slowly started to feel better and better, until at some point '
    msg += 'the bad feeling was completely gone!\n'
    msg += '**You have turned into an Innocent and you are no longer a Cursed Civlian. The rules remain the same, '
    msg += 'you will just no longer turn into a wolf.**'

    if old_role == 'Cursed Civilian':
        return msg

    return "This is weird! This DM should've been different!"

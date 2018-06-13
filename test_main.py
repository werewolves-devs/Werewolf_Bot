# This file runs CI on Travis
# It will be better soon
from management.position import positionof
import management.db as db
import reset

# Sanity checks
def test_universe_is_working_properly():
  assert 1 == 1 #If this fails, something is seriously wrong
  assert True != False # Making sure
  assert 1 == 1 # If this fails, something is seriously wrong
  assert str(1) == "1" #Make sure python 6 hasn't released and changed all the names like minecraft did in 1.13 like seriously what was wrong with the old system there was nothing wrong with it why do I have to learn an entirely new system that I don't aaaaaaaaaaaa

# Check positionof() function
def test_positionof():
  assert positionof("frozen") == 13
  assert positionof("fakerole") == 6
  assert positionof("votes") == 8
  assert positionof("sleepers") == 19
  assert positionof("bitten") == 16
  assert positionof("id") == 0
# There isn't actually any other tests yet

def kill_queue_test():
  db.add_kill(12738912739821,"Barber")
  db.add_kill(12347892374923,"White Werewolf","7289347983274")
  assert db.get_kill() == [1,u'12738912739821',u'Barber',u'']
  assert db.get_kill() == [2,u'12347892374923',u'White Werewolf',u'7289347983274']
  assert db.get_kill() == None
  reset.reset(True)
  return True

# Check the database
def test_database():
  assert poll_list() == []
  db.signup(1,'Randium003',u':smirk:')
  assert get_user(1) == (u'1', u'Randium003', u':smirk:', 0, u'#gamelog', u'Spectator', u'Spectator', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, u'', u'', u'', u'')
  assert db_get(1,'channel') == '#gamelog'
  assert isParticipant(1) == True
  assert isParticipant(2) == False
  db_set(1,'frozen',1)
  assert poll_list() == [(u'1',u'Randium003',u'1')]

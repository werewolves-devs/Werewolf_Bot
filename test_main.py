# This file runs CI on Travis
# It will be better soon
from management.db import db_test
from management.position import positionof

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

# Check if the kill_queue is fully functional
import management.db as db
import reset

def kill_queue_test():
  db.add_kill(12738912739821,"Barber")
  db.add_kill(12347892374923,"White Werewolf","7289347983274")
  assert db.get_kill() == [1,u'12738912739821',u'Barber',u'']
  assert db.get_kill() == [2,u'12347892374923',u'White Werewolf',u'7289347983274']
  assert db.get_kill() == None
  reset.reset(True)
  return True

# This file runs CI on Travis
# It will be better soon
from management.position import positionof
import interpretation.check as check
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
  reset.reset(True)
  assert db.count_categories() == 0
  assert db.get_category() == None
  assert db.get_columns() == []
  assert db.poll_list() == []
  db.signup(1,'Randium003',u':smirk:')
  assert db.get_user(1) == (u'1', u'Randium003', u':smirk:', 0, u'#gamelog', u'Spectator', u'Spectator', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, u'', u'', u'', u'',0)
  assert db.db_get(1,'channel') == '#gamelog'
  assert db.isParticipant(1) == False
  assert db.isParticipant(1,True) == True
  assert db.isParticipant(2) == False
  assert db.isParticipant(2,True) == False
  db.db_set(1,'frozen',1)
  assert db.poll_list() == [(u'1',u':smirk:',1,0)]

  db.add_category('24')
  assert db.count_categories() == 1
  assert db.get_category() == 24
  assert db.get_columns() == [(u'1',)]
  assert db.channel_get('1234555') == None
  db.add_channel('1234555',1)
  assert db.get_category() == 24
  db.add_channel('12211',1)
  assert db.get_category() == 24
  assert db.channel_get('1234555') == (u'1234555',u'1',u'0')
  assert db.channel_change_all(1,0,1) == [u'1234555',u'12211']
  assert db.channel_get('1234555') == (u'1234555',u'1',u'1')
  assert db.channel_get('12211') == (u'12211',u'1',u'1')
  db.set_user_in_channel('1234555',1,2)
  assert db.channel_get('1234555') == (u'1234555',u'1',u'2')
  assert db.channel_get('1234555',1) == (u'2',)
  assert db.channel_change_all(1,2,3) == [u'1234555']
  assert db.unabduct(1) == [u'1234555']
  db.signup(420,"BenTechy66",":poop:")
  assert db.channel_get('12211') == (u'12211',u'1',u'1',u'0')
  assert db.freeze('1') == [u'1234555',u'12211']
  assert db.abduct('420') == []

  for i in range(48):
    assert db.get_category() == 24
    db.add_channel(10*i,608435446804+7864467*i)
  assert db.count_categories() == 1
  assert db.get_category() == None
  reset.reset(True)

  
# Make sure the check module is working as intended
def check_check():
  class message:
    content = "Deze tekst is Nederlands, maar bevat 4 cijfers; 1999 8 en 1 ! Jazeker, dat zijn er vier. Zoiets zou een Hooker zoals jij nooit opmerken."

  x = message()
  assert check.numbers(x) == [4,1999,8,1]
  assert check.numbers(x,3) == [4,1999,8]
  assert check.numbers(x,5) == False
  assert check.emojis(x) == False
  assert check.roles(x) == ['Hooker']
  assert check.roles(x,1) == ['Hooker']
  assert check.roles(x,2) == False

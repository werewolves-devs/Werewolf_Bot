# This file runs CI on Travis
# It will be better soon
from config import max_channels_per_category, game_log
from management.position import positionof
from main_classes import Mailbox
import roles_n_rules.switch as switch
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
  assert positionof("sleepingover") == 18
  assert positionof("bitten") == 16
  assert positionof("id") == 0

def test_kill_queue():
  reset.reset(True)
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
  assert db.get_user(1) == (1, u'Randium003', u':smirk:', 0, game_log, 'Spectator', 'Spectator', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, '', 0, 0, 0)
  assert db.db_get(1,'channel') == game_log
  assert db.isParticipant(1) == False
  assert db.isParticipant(1,True) == True
  assert db.isParticipant(2) == False
  assert db.isParticipant(2,True) == False
  db.db_set(1,'frozen',1)
  assert db.poll_list() == [(1,u':smirk:',1,0)]

  db.add_category('24')
  assert db.count_categories() == 1
  assert db.get_category() == 24
  assert db.get_columns() == [(1,)]
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
  assert db.channel_get('1234555',1) == '2'
  assert db.channel_change_all(1,2,3) == [u'1234555']
  db.signup(420,"BenTechy66",":poop:")
  assert db.channel_get('12211') == (u'12211',u'1',u'1',u'0')

  for i in range(max_channels_per_category - 2):
    assert db.get_category() == 24
    db.add_channel(10*i,608435446804+7864467*i)
  assert db.count_categories() == 1
  assert db.get_category() == None
  reset.reset(True)


# Make sure the check module is working as intended
def test_check():
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

def test_control_freezers():
  reset.reset(True)
  assert db.add_freezer(1,3,'Pyromancer') == None
  assert db.add_freezer(1,3,'The Thing') == 'Pyromancer'
  assert db.add_freezer(1,4,'Assassin') == None
  assert db.add_freezer(1,3,'Booh') == 'The Thing'
  assert db.add_freezer(1,5,'Hooker') == None
  assert db.add_freezer(2,9,'Fortune Teller') == None
  assert db.get_freezers(1) == [(3, 'Booh'), (4, 'Assassin'), (5, 'Hooker')]
  assert db.delete_freezer(1,7) == False
  assert db.delete_freezer(1,4) == True
  assert db.get_freezers(1) == [(3, 'Booh'), (5, 'Hooker')]
  reset.reset(True)

def test_mexican():
  reset.reset(True)
  db.add_standoff(2,'Huntress',1)
  db.add_standoff(3,'Cupid',1)
  db.add_standoff(1,'Cupid',3)
  print(db.get_standoff(3))
  print(db.get_standoff(1))
  assert db.get_standoff(3) == [[3,'1','Cupid','3']]
  assert db.get_standoff(1) == [[1,'2','Huntress','1'],[2,'3','Cupid','1']]
  db.delete_standoff(2)
  assert db.get_standoff(1) == [[1,'2','Huntress','1']]
  reset.reset(True)

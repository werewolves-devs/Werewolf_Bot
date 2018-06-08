from management.db import db_test

#This file runs CI on Travis
# It will be better soon

def test_universe_is_working_properly():
  assert 1 == 1 #If this fails, something is seriously wrong

  assert db_test() == 'Randium003'

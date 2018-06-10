from management.db import db_test
from management.position import positionof

#This file runs CI on Travis
# It will be better soon

def test_universe_is_working_properly():
  assert 1 == 1 #If this fails, something is seriously wrong

  assert db_test() == 'Randium003'

  assert positionof("frozen") == 13
  assert positionof("fakerole") == 6
  assert positionof("votes") == 8
  assert positionof("sleepers") == 19
  assert positionof("bitten") == 16
  assert positionof("id") == 0

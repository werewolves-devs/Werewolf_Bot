from test import database_check

#This file runs CI on Travis
# It will be better soon

def test_universe_is_working_properly():
  assert 1 == 1 #If this fails, something is seriously wrong

  # WARNING: DO NOT EXECUTE DURING A GAME
  assert database_check() == 'Assassin'

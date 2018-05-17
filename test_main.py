# This file runs CI on Travis
# It will be better soon

# Sanity checks
def test_universe_is_working_properly():
  assert True != False # Making sure
  assert 1 == 1 # If this fails, something is seriously wrong
  assert str(1) == "1" #Make sure python 6 hasn't released and changed all the names like minecraft did in 1.13 like seriously what was wrong with the old system there was nothing wrong with it why do I have to learn an entirely new system that I don't aaaaaaaaaaaa


# Functions module checks
import functions
def test_functions_module():
    assert functions.check_for_int(5) == True
    assert functions.check_for_int("absudHBASH") == False
    assert functions.check_for_int("5") == True


# There isn't actually anything else to check

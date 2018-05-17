# This file runs CI on Travis
# It will be better soon

# Sanity checks
def test_universe_is_working_properly():
  assert 1 == 1 #If this fails, something is seriously wrong


# Functions module checks
import functions
def test_functions_module():
    assert functions.check_for_int(5) == True
    assert functions.check_for_int("absudHBASH") == False
    assert functions.check_for_int("5") == True

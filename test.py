from roles_n_rules.roles import Executioner, get_powers, role_functions, Team
from story_time.reader import import_story, player_amount, import_random_story
from management.player import Player, Participant
from config import Destination
import unittest


class User:
    def __init__(self,id,name,bot):
        self.id = id
        self.name = name
        self.bot = bot

class Test_Player_Class(unittest.TestCase):

    def test_threats(self):
        player1 = Participant(User(1,"Randium",False))

        self.assertEqual(player1.id,1)
        self.assertEqual(player1.channel,485843514379337748)
        self.assertEqual(player1.threatened,0)

        player1.threatened = 1
        self.assertEqual(player1.threatened,1)
        
        player1.threatened += 3
        self.assertEqual(player1.threatened,4)

        player2 = Participant(User(1,"Randium",False))
        self.assertEqual(player1.threatened,player2.threatened)
        player2.threatened = 0
    
    def test_enchantments(self):
        player1 = Participant(User(1,"Randium",False))

        self.assertEqual(player1.id,1)
        self.assertEqual(player1.channel,485843514379337748)
        self.assertEqual(player1.enchanted,False)

        player1.enchanted = True
        self.assertEqual(player1.enchanted,True)
        
        player2 = Participant(User(1,"Randium",False))
        self.assertEqual(player1.enchanted,player2.enchanted)
        player2.enchanted = False
    
    def test_demonized(self):
        player1 = Participant(User(1,"Randium",False))

        self.assertEqual(player1.id,1)
        self.assertEqual(player1.channel,485843514379337748)
        self.assertEqual(player1.demonized,False)

        player1.demonized = True
        self.assertEqual(player1.demonized,True)
        
        player2 = Participant(User(1,"Randium",False))
        self.assertEqual(player1.demonized,player2.demonized)
        player2.demonized = False

    def test_role_properties(self):
        self.assertEqual([item for item in Executioner.__dict__ if item.startswith('st')],['start'])
        self.assertEqual(get_powers("Executioner"),['execute'])
        self.assertEqual(role_functions("Grandma").team,Team.village)
    
    def test_config(self):
        int(Destination.game_log.value)
        with self.assertRaises(TypeError):
            int(Destination.game_log)
    
    def test_story_time_reader(self):
        self.assertEqual(import_story('unittests/001.txt'),'This is a simple test!')
        self.assertEqual(import_story('unittests/002.txt',owner='BenTechy66'),'This is a slightly more advanced test.\nAin\'t that right, BenTechy66?')
        self.assertEqual(import_story('unittests/003.txt',player_list=['Randium','HurricanKai']),'I was told by Randium and HurricanKai that this would work.\nRandium even promised me!')

        self.assertEqual(player_amount('unittests/001.txt'),0)
        self.assertEqual(player_amount('unittests/002.txt'),0)
        self.assertEqual(player_amount('unittests/003.txt'),2)

        self.assertEqual(import_random_story('unittests/',player_list=['Randium','HurricanKai']),"I was told by <@Randium> and <@HurricanKai> that this would work.\n<@Randium> even promised me!")
        self.assertEqual(import_random_story('unittests',player_list=['Yo momma']),'I am terribly sorry! I could not find a story for this!')

        # Unorthodox tests
        self.assertEqual(import_story('unittests/002.txt',player_list=['BenTechy66']),'This is a slightly more advanced test.\nAin\'t that right, UNDEFINED?')
        self.assertEqual(import_story('unittests/003.txt',owner='Randium'),'I was told by [0] and [1] that this would work.\n[0] even promised me!')
        self.assertEqual(import_story('unittests/003.txt',player_list=['Randium','HurricanKai','BenTechy66']),'I was told by Randium and HurricanKai that this would work.\nRandium even promised me!')


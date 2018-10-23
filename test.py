from roles_n_rules.roles import Executioner, get_powers, role_functions, Team
from story_time.reader import import_story, player_amount, import_random_story
from management.player import Player, Participant
from hardcore_reset import new_database_required
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

    def test_money(self):
        player1 = Participant(User(1,"Randium",False))
        player1.money = 0
        self.assertEqual(player1.money,0)
        player1.money = 1000
        self.assertEqual(player1.money,1000)
        player1.money += 40
        self.assertEqual(player1.money,1040)
        
        player2 = Participant(User(1,"Randium",False))
        self.assertEqual(player2.money,1040)
        player2.money = 0
        self.assertEqual(player1.money,0)

    def _inventory(self):
        # To be claimed: 1 lootbox
        player1 = Participant(User(1,"Randium",False))

        self.assertEqual(player1.items,[])

        player1.add(1)
        player1.add("villager buck")
        self.assertEqual(player1.items,[(1,'villager buck',2)])

        player1.add(2)
        player1.add(2)
        player1.remove(1)
        player1.remove(3) # ! Make sure it doesn't give the user a negative amount.
        self.assertEqual(player1.items,[(1,'villager buck',1),(2,'wolf buck',2)])

        player2 = Participant(User(1,"Randium",False))
        self.assertEqual(player1.items,player2.items)
    
        player1.remove(1)
        player1.remove(2)
        player1.remove(2)
        self.assertEqual(player2.items,[])

    @new_database_required
    def _auto_registration(self):
        # To be claimed: 1 lootbox
        # The point of this function is to make sure that a player is added to the database if they do not exist yet.
        # Note that they get added to the general database; they do not get signed up.
        # See the __init__ function of the Player class.
        
        player1 = Player(User(1,"Randium",False))
        self.assertEqual(player1.money,0)
        self.assertEqual(player1.items,[])
        self.money = 100
        
        player2 = Player(User(1,"Randium",False))
        self.assertEqual(player2.money,100)


    def test_role_properties(self):
        self.assertEqual([item for item in Executioner.__dict__ if item.startswith('st')],['start'])
        self.assertEqual(get_powers("Executioner"),['execute'])
        self.assertEqual(role_functions("Grandma").team,Team.village)
    
    def test_config(self):
        int(Destination.game_log.value)
        with self.assertRaises(TypeError):
            int(Destination.game_log)
    

class Test_Story_Time(unittest.TestCase):
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


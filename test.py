from roles_n_rules.roles import Executioner, get_powers, role_functions, Team
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
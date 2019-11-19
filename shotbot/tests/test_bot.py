import unittest
from bot import Bot

class TestBot(unittest.TestCase):
    shotbot = Bot("test")
    def test_is_initialized(self):
        self.assertTrue(isinstance(self.shotbot, Bot))
        self.assertTrue(self.shotbot.get_name()=="test")
        
    def test_relays_configured(self):
        self.assertEqual(len(self.shotbot.get_relays()), 6)

    def test_default_target(self):
        #test default target
        self.assertEqual(self.shotbot.get_target(), [2,2])

    def test_target_outofbounds(self):
        self.shotbot.set_target(2,2)
        self.shotbot.get_target(), [2,2]
        with self.assertRaises(ValueError) as cm:
            self.shotbot.set_target(4,4)
        with self.assertRaises(ValueError) as cm:
            self.shotbot.set_target(0,-1)
        self.assertEqual(self.shotbot.get_target(), [2,2])

    def test_target_moves(self):
        self.assertEqual(self.shotbot.get_target(), [2,2])
        #test one move to the left
        move = self.shotbot.set_target(1,2)
        self.assertEqual(move, [-1,0])
        #test two moves to the right
        move = self.shotbot.set_target(3,2)
        self.assertEqual(move, [2,0])
        #test move up 1
        move = self.shotbot.set_target(3,3)
        self.assertEqual(move, [0,1])
        #test move down 2
        move = self.shotbot.set_target(3,1)
        self.assertEqual(move, [0,-2])
        move = self.shotbot.set_target(1,3)
        self.assertEqual(move, [-2,2])

if __name__ == '__main__': 
    unittest.main() 
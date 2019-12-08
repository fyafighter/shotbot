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
        self.shotbot.get_target()
        with self.assertRaises(ValueError) as cm:
            self.shotbot.set_target(4,4)
        with self.assertRaises(ValueError) as cm:
            self.shotbot.set_target(0,-1)
        self.assertEqual(self.shotbot.get_target(), [2,2])

    def test_target_moves(self):
        self.assertEqual(self.shotbot.get_target(), [2,2])
        #test one move to the left
        move = self.shotbot.set_target(1,2)
        self.assertEqual(move, [-1,0,3])
        #test two moves to the right
        move = self.shotbot.set_target(3,2)
        self.assertEqual(move, [2,0,6])
        #test move up 1
        move = self.shotbot.set_target(3,3)
        self.assertEqual(move, [0,1,3])
        #test move down 2
        move = self.shotbot.set_target(3,1)
        self.assertEqual(move, [0,-2,6])
        move = self.shotbot.set_target(1,3)
        self.assertEqual(move, [-2,2,6])
    
    def test_target_relays(self):
        self.shotbot.set_target(2,2)
        move = self.shotbot.set_target(3,2)
        self.assertEqual(move, [1,0,3])
        self.assertEqual(self.shotbot.relays['right'].state, 1)
        self.assertTrue(self.shotbot.relays['right'].time_remaining()>1)
        self.assertTrue(self.shotbot.relays['right'].timer.is_alive())
        move = self.shotbot.set_target(1,2)
        self.assertEqual(move, [-2,0,6])
        self.assertEqual(self.shotbot.relays['left'].state, 1)
        self.assertTrue(self.shotbot.relays['left'].time_remaining()>4)
        self.assertTrue(self.shotbot.relays['left'].timer.is_alive())
    
    def test_calibration(self):
        self.shotbot.set_target(3,3)
        self.assertEqual(self.shotbot.get_target(), [3,3])
        self.shotbot.calibrate_center()
        self.assertEqual(self.shotbot.get_target(), [2,2])

    def test_manual_move(self):
        self.shotbot.manual_move("up", 5)
        self.assertEqual(self.shotbot.relays['up'].state, 1)
        self.assertTrue(self.shotbot.relays['up'].timer.is_alive())
        self.assertTrue(self.shotbot.relays['up'].time_remaining()>3)
        
if __name__ == '__main__': 
    unittest.main() 
import unittest
from relay import Relay
import time

class TestRelays(unittest.TestCase):
    relay = Relay("pan", 1, 2)
    def test_is_initialized(self):
        self.assertTrue(isinstance(self.relay, Relay))
        self.assertTrue(self.relay.name=="pan")
    
    def test_relay_change(self):
        self.assertEqual(self.relay.state, 0)
        self.relay.switchOn()
        self.assertEqual(self.relay.state, 1)
        self.relay.switchOff()
        self.assertEqual(self.relay.state, 0)
        self.relay.switch()
        self.assertEqual(self.relay.state, 1)
        self.relay.switch()
        self.assertEqual(self.relay.state, 0)
    
    def test_relay_timeouts(self):
        self.assertFalse(self.relay.timer.is_alive())
        self.relay.switchOn()
        self.assertTrue(self.relay.timer.is_alive())
        time.sleep(3)
        self.assertFalse(self.relay.timer.is_alive())
        self.relay.switchOn()
        self.assertTrue(self.relay.time_remaining()>0)
        time.sleep(2.5)
        self.assertFalse(self.relay.timer.is_alive())
        self.assertTrue(self.relay.time_remaining()==0)
if __name__ == '__main__': 
    unittest.main() 
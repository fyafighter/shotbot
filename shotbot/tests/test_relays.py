import unittest
from relay import Relay
import time

class TestRelays(unittest.TestCase):
    relay = Relay("relay_test", 1, 5)
    def test_is_initialized(self):
        self.assertTrue(isinstance(self.relay, Relay))
        self.assertTrue(self.relay.name=="relay_test")
    
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
        relay = Relay("default_timeout_test", 2, 5)
        relay.switchOn()
        self.assertTrue(relay.timer.is_alive())
        self.assertTrue(relay.time_remaining()>0)
        time.sleep(5.1)
        self.assertFalse(relay.timer.is_alive())
        self.assertTrue(relay.time_remaining()==0)
        relay.switchOn()
        self.assertTrue(relay.time_remaining()>3)
        time.sleep(2)
        relay.switchOn()
        self.assertTrue(relay.time_remaining()>3)

    def testTimedSwitch(self):
        relay = Relay("timeout_test", 3, 5)
        relay.switchOn(8)
        self.assertTrue(relay.time_remaining()>6)
        self.assertTrue(relay.timer.is_alive())
        time.sleep(8.1)
        self.assertFalse(relay.timer.is_alive())

if __name__ == '__main__': 
    unittest.main() 
import unittest
from relay import Relay

class TestRelays(unittest.TestCase):
    relay = Relay("pan", 1, 5)
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
        self.relay.switchOn()

if __name__ == '__main__': 
    unittest.main() 
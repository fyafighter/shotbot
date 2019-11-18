from unittest import TestCase
from ..shotbot import Shotbot

class TestShotbot(TestCase):
    def test_is_initialized(self):
        s = Shotbot("test")
        self.assertTrue(isinstance(s, Shotbot))
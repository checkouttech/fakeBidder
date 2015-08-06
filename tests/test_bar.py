import unittest
import sys,os
sys.path.insert(0,os.path.abspath(__file__+"/../.."))

from foo import bar

class TestBar(unittest.TestCase):
    def test_bar_true(self):
        self.assertTrue(bar.dumb_true())

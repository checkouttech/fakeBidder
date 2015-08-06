import unittest
import sys,os

from fakebidder import bar

class TestBar(unittest.TestCase):
    def test_bar_true(self):
        self.assertTrue(bar.dumb_true())

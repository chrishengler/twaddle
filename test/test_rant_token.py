import unittest

from pyrant.rant_token import RantToken, RantTokenType

class RantTokenTest(unittest.TestCase):
    def testRantTokenEquality(self):
        plaintext = RantToken(RantTokenType.PLAIN_TEXT,"plaintext")
        different_plaintext = RantToken(RantTokenType.PLAIN_TEXT,"different plaintext")
        left_angle = RantToken(RantTokenType.LEFT_ANGLE_BRACKET)

        self.assertEqual(plaintext,plaintext)
        self.assertNotEqual(plaintext, left_angle)
        self.assertNotEqual(plaintext, different_plaintext)


import unittest

from rant_token import RantToken, RantTokenType

class RantTokenTest(unittest.TestCase):
    def testRantTokenEquality(self):
        plaintext = RantToken(RantTokenType.PLAIN_TEXT,"plaintext")
        duplicate_plaintext = RantToken(RantTokenType.PLAIN_TEXT,"plaintext")
        different_plaintext = RantToken(RantTokenType.PLAIN_TEXT,"different plaintext")
        empty_plaintext = RantToken(RantTokenType.PLAIN_TEXT)
        left_angle = RantToken(RantTokenType.LEFT_ANGLE_BRACKET)
        hyphen = RantToken(RantTokenType.HYPHEN)


        self.assertEqual(plaintext,duplicate_plaintext)
        self.assertNotEqual(plaintext,empty_plaintext)
        self.assertNotEqual(plaintext,left_angle)
        self.assertNotEqual(plaintext,different_plaintext)
        self.assertNotEqual(left_angle,hyphen)


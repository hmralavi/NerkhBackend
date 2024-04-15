import unittest
from datetime import timedelta
import time
import sys

sys.path.append("src")

from authentication_tools import generate_token, validate_token


class TestToken(unittest.TestCase):

    def test_valid_token(self):
        """
        create a token and check if it's valid
        """
        username = "testuser"
        token = generate_token(username)
        auth = validate_token(token)
        self.assertTrue(auth[0])
        self.assertEqual(auth[1], "Token is valid")
        self.assertEqual(auth[2], username)

    def test_invalid_token(self):
        """
        create a token and modify it. the resulting token should be invalid
        """
        username = "testuser"
        token = generate_token(username)
        token = token[:-4] + "qwer"
        auth = validate_token(token)
        self.assertFalse(auth[0])
        self.assertEqual(auth[1], "Invalid token")

    def test_expired_token(self):
        """
        create a token with expiration duration o 1 second. so 2 seconds later,
        the token should be invalid.
        """
        username = "testuser"
        exp_dur = timedelta(seconds=1)
        token = generate_token(username, exp_dur)
        time.sleep(2)
        auth = validate_token(token)
        self.assertFalse(auth[0])
        self.assertEqual(auth[1], "Token has expired")


if __name__ == "__main__":
    unittest.main()

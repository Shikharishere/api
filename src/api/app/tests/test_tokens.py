"""
    Tests tokens (Access token) unit.
"""


import unittest

from app.tokens import AccessToken


class TestAccessTokenUnit(unittest.TestCase):
    """Tests access token token unit."""

    def test_access_token_unsigned(self):
        """Test encoding without signature (key)"""
        key = "my_secret_key"
        token = AccessToken("me", 1, 2, 3, "", key=key)

        decoded_unsigned_token = AccessToken.decode(token.encode())
        self.assertFalse(decoded_unsigned_token.signature_is_valid())

        decoded_signed_token = AccessToken.decode(token.encode(), key=key)
        self.assertTrue(decoded_signed_token.signature_is_valid())

        self.assertEqual(
            decoded_unsigned_token.get_subject(), decoded_signed_token.get_subject()
        )
        self.assertEqual(
            decoded_unsigned_token.get_session_id(),  # pylint: disable=no-member
            decoded_signed_token.get_session_id(),  # pylint: disable=no-member
        )

    def test_access_token(self):
        """Test base feature."""
        key = "my_secret_key"
        token = AccessToken("me", 1, 2, 3, "", key=key)
        encoded_token = token.encode()
        decoded_token = AccessToken.decode(encoded_token, key)
        self.assertEqual(
            AccessToken.decode(encoded_token, key).get_raw_payload(),
            decoded_token.get_raw_payload(),
        )

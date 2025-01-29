# File: test/test_chat.py
# Description: Unit tests for the /chat endpoint.

import unittest
import requests


class TestChatEndpoint(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000"

    def test_chat_endpoint_valid_query(self):
        """
        Test the /chat endpoint with a valid query.
        """
        response = requests.post(
            f"{self.BASE_URL}/chat",
            json={"query": "What role did the Little Rock Arsenal play in the Civil War?"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("answer", response.json())
        self.assertIn("top_chunks", response.json())

    def test_chat_endpoint_empty_query(self):
        """
        Test the /chat endpoint with an empty query.
        """
        response = requests.post(
            f"{self.BASE_URL}/chat",
            json={"query": ""}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_chat_endpoint_invalid_payload(self):
        """
        Test the /chat endpoint with an invalid payload.
        """
        response = requests.post(
            f"{self.BASE_URL}/chat",
            json={"invalid_key": "invalid_value"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())


if __name__ == "__main__":
    unittest.main()

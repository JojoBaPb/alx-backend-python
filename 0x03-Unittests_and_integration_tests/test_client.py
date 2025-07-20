#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient.org"""
import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `org` property of GithubOrgClient"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test that GithubOrgClient.org returns expected result"""
        expected_payload = {"login": "google", "id": 123}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("google")
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")


if __name__ == '__main__':
    unittest.main()

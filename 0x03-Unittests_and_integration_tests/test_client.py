#!/usr/bin/env python3
"""Unit and integration tests for client.py"""
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient.org method"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test that GithubOrgClient.org returns correct payload"""
        test_payload = {"login": "google", "id": 1}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("google")
        self.assertEqual(client.org, test_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")


if __name__ == '__main__':
    unittest.main()

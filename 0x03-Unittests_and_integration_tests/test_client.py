#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient.org"""
import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the GithubOrgClient class"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test that GithubOrgClient.org returns expected result"""
        expected_payload = {"login": "google", "id": 123}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("google")
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")

    def test_has_memoize_decorator(self):
        """Check if org method is memoized"""
        self.assertTrue(hasattr(GithubOrgClient.org, '__wrapped__'))

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json):
        """Test the _public_repos_url property"""
        payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_get_json.return_value = payload

        client = GithubOrgClient("google")
        self.assertEqual(client._public_repos_url, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method"""
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repos_payload

        with patch.object(GithubOrgClient, 'repos_payload', new_callable=PropertyMock) as mock_payload:
            mock_payload.return_value = repos_payload
            client = GithubOrgClient("google")

            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            self.assertEqual(client.public_repos(license="mit"), ["repo1"])
            self.assertEqual(client.public_repos(license="apache-2.0"), ["repo2"])
            self.assertEqual(client.public_repos(license="gpl"), [])


if __name__ == '__main__':
    unittest.main()

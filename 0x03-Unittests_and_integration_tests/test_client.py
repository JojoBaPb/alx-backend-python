#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient.org"""
import unittest
from unittest.mock import patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload, "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Test class for integration tests with external API calls"""

    @classmethod
    def setUpClass(cls):
        """Set up mock patchers for external requests"""
        cls.get_patcher = patch('client.requests.get')
        cls.mock_get = cls.get_patcher.start()

        # Mock the requests.get response
        cls.mock_get.side_effect = lambda url: {
            "https://api.github.com/orgs/google": cls.org_payload,
            "https://api.github.com/orgs/google/repos": cls.repos_payload,
            "https://api.github.com/orgs/facebook": cls.org_payload,
            "https://api.github.com/orgs/facebook/repos": cls.repos_payload,
        }.get(url)

    @classmethod
    def tearDownClass(cls):
        """Stop the mock patchers"""
        cls.get_patcher.stop()

    @parameterized.expand([
        ("google", "repos_url"),
        ("facebook", "repos_url")
    ])
    def test_integration(self, org, repos_url):
        """Test integration of public_repos method"""
        self.mock_get.return_value.json.return_value = {"repos_url": repos_url}

        client = GithubOrgClient(org)
        self.assertEqual(client._public_repos_url, repos_url)


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the `GithubOrgClient` class"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test that GithubOrgClient.org returns expected result"""
        expected_payload = {"login": "google", "id": 123}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("google")
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google")

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', return_value="https://api.github.com/orgs/google/repos")
    def test_public_repos_url(self, mock_public_repos_url, mock_get_json):
        """Test that _public_repos_url returns the expected result with mock"""
        expected_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, expected_payload["repos_url"])
        mock_get_json.assert_called_once_with(expected_payload["repos_url"])

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url', return_value="https://api.github.com/orgs/google/repos")
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test that public_repos returns the expected result"""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, ["repo1", "repo2"])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test has_license method with different inputs"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

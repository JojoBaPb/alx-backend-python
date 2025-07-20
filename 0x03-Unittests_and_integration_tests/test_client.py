#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient

# Fixtures
ORG_PAYLOAD = {"repos_url": "https://api.github.com/orgs/google/repos"}
REPOS_PAYLOAD = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]
EXPECTED_REPOS = ["repo1", "repo2", "repo3"]
APACHE2_REPOS = ["repo1", "repo3"]

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @patch('client.get_json')
    def test_public_repos_url(self, mock_get_json):
        """Test that _public_repos_url returns the expected URL based on the mocked org"""
        expected_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient("google")
        result = client._public_repos_url

        self.assertEqual(result, expected_payload["repos_url"])

    @patch('client.get_json')
    @patch.object(GithubOrgClient, 'org', return_value=ORG_PAYLOAD)
    def test_public_repos(self, mock_org, mock_get_json):
        """Test public_repos() with mocked get_json and _public_repos_url"""
        mock_get_json.return_value = REPOS_PAYLOAD

        client = GithubOrgClient("google")
        result = client.public_repos()

        # Assert that the result is what we expect
        self.assertEqual(result, EXPECTED_REPOS)

        # Assert the mocked methods were called once
        mock_get_json.assert_called_once_with(ORG_PAYLOAD["repos_url"])
        mock_org.assert_called_once()

    @parameterized_class([
        {
            'repo': {"license": {"key": "my_license"}},
            'license_key': "my_license",
            'expected': True
        },
        {
            'repo': {"license": {"key": "other_license"}},
            'license_key': "my_license",
            'expected': False
        }
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license method"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

@parameterized_class([
    {
        'org_payload': ORG_PAYLOAD,
        'repos_payload': REPOS_PAYLOAD,
        'expected_repos': EXPECTED_REPOS,
        'apache2_repos': APACHE2_REPOS
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test class for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: cls.org_payload),
            unittest.mock.Mock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos() using integration testing"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with a specific license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)

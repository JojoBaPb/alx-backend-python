#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient.org"""
import unittest
from unittest.mock import patch, MagicMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the `GithubOrgClient` class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method returns correct payload"""
        mock_get_json.return_value = org_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, org_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url works as expected"""
        with patch.object(GithubOrgClient, 'org', new_callable=MagicMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://some_url"}
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, "http://some_url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method returns correct list of repo names"""
        mock_get_json.return_value = repos_payload
        with patch.object(GithubOrgClient, '_public_repos_url', return_value="http://some_url"):
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), expected_repos)
            mock_get_json.assert_called_once_with("http://some_url")

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos returns only repos with given license"""
        mock_get_json.return_value = repos_payload
        with patch.object(GithubOrgClient, '_public_repos_url', return_value="http://some_url"):
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(license="apache-2.0"), apache2_repos)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license static method"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class((
    'org_payload',
    'repos_payload',
    'expected_repos',
    'apache2_repos'
), [
    (org_payload, repos_payload, expected_repos, apache2_repos)
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using actual data"""

    @classmethod
    def setUpClass(cls):
        """Set up class-wide mocks"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
        ]

    @classmethod
    def tearDownClass(cls):
        """Tear down patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos method"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)


if __name__ == '__main__':
    unittest.main()

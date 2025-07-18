#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org returns correct payload and get_json called once."""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns repos_url from .org property."""
        expected_url = "https://api.github.com/orgs/google/repos"
        mocked_org_payload = {"repos_url": expected_url}
        client = GithubOrgClient("google")

        with patch.object(
            GithubOrgClient, "org", new_callable=property
        ) as mock_org:
            mock_org.return_value = mocked_org_payload
            result = client._public_repos_url
            self.assertEqual(result, expected_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns correct repo names list."""
        test_repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos_payload

        client = GithubOrgClient("test_org")
        test_url = "https://api.github.com/orgs/test_org/repos"

        with patch.object(
                GithubOrgClient,
                "_public_repos_url",
                new_callable=property) as mock_public_repos_url:

            mock_public_repos_url.return_value = test_url

            repos = client.public_repos()
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(repos, expected_repos)

            # Since mock_public_repos_url is a patch on a property,
            #  assert_called_once()
            # does not always work as expected. Instead check call count:
            self.assertEqual(mock_public_repos_url.call_count, 1)

            mock_get_json.assert_called_once_with(test_url)


if __name__ == "__main__":
    unittest.main()

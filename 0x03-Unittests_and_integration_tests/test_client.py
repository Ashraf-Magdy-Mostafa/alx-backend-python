#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.org property."""

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
        """Test GithubOrgClient._public_repos_url property returns repos_url from org."""
        expected_url = "https://api.github.com/orgs/google/repos"
        mocked_org_payload = {"repos_url": expected_url}

        client = GithubOrgClient("google")

        # Patch the 'org' property to return our mocked_org_payload
        with patch.object(GithubOrgClient, "org", new_callable=property) as mock_org:
            mock_org.return_value = mocked_org_payload

            # Now accessing _public_repos_url should use the mocked org property
            result = client._public_repos_url
            self.assertEqual(result, expected_url)

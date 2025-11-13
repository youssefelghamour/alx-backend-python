#!/usr/bin/env python3
"""A unittest for GithubOrgClient"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        "google",
        "abc",
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Tests org method of GithubOrgClient
            - Mocks get_json to return a specific payload
            - Asserts that get_json is called with the expected URL
            - Asserts that the org method returns the expected payload
        """
        # Set the mock to return a specific value
        mock_get_json.return_value = {"org": org_name}

        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Call the org property (because of @memoize, it's a property)
        result = client.org

        # Assert that get_json was called with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

        # Assert that the result is as expected
        self.assertEqual(result, {"org": org_name})

    def test_public_repos_url(self) -> None:
        """Tests _public_repos_url property of GithubOrgClient
            - Mocks the org property to return a specific payload
            - Asserts that _public_repos_url returns the expected URL
        """
        # memoize makes org a property, so we patch it as a PropertyMock
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            # Set the mock to return a specific value
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("google")

            # Access the _public_repos_url property
            result = client._public_repos_url

            # Assert that the result is as expected
            self.assertEqual(result,
                             "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json) -> None:
        """Tests public_repos method of GithubOrgClient
            - Mocks the get_json function to return a specific payload
            - Mocks the repos_payload property to return a specific payload
            - Asserts that public_repos returns the expected list of repo names

            public_repos() calls repos_payload, which calls get_json with
            _public_repos_url. That's why we mock everything
        """
        # Mock get_json (used by repos_payload) to avoid making a real API call
        mock_get_json.return_value = TEST_PAYLOAD[0][1]

        # Mock _public_repos_url property because it is used in repos_payload
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_publc_repos_url:
            # Set the mock to return a specific repos_url
            # "https://api.github.com/orgs/google/repos"
            mock_publc_repos_url.return_value = TEST_PAYLOAD[0][0]["repos_url"]

            # Create an instance of GithubOrgClient
            client = GithubOrgClient("google")

            # Call the public_repos method
            # It should use the result of the mocked get_json
            # and return the list of repo names
            result = client.public_repos()

            # Assert that the result is as expected
            self.assertEqual(result, TEST_PAYLOAD[0][2])

            mock_publc_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                TEST_PAYLOAD[0][0]["repos_url"])


if __name__ == "__main__":
    unittest.main()

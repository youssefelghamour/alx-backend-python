#!/usr/bin/env python3
"""A unittest for GithubOrgClient"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


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


if __name__ == "__main__":
    unittest.main()

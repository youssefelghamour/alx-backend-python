#!/usr/bin/env python3
""" Unittests for the functions in client module """
import unittest
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, Mock, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """ tests the GithubOrgClient class """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock):
        """ tests the org function """
        # create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # call the org method
        client.org()

        # assert get_json was called once with the expected URL
        mock.assert_called_once_with(f'https://api.github.com/orgs/{org_name}')

    def test_public_repos_url(self):
        """ tests _public_repos_url function """
        # create an instance of GithubOrgClient
        test_client = GithubOrgClient("google")

        # mock the org property with PropertyMock
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mck_org:
            mck_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }

            res = test_client._public_repos_url
            # assert _public_repos_url returns the expected value
            self.assertEqual(res, "https://api.github.com/orgs/google/repos")


if __name__ == "__main__":
    unittest.main()

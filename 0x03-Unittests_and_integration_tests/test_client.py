#!/usr/bin/env python3
""" Unittests for the functions in client module """
import unittest
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, Mock


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


if __name__ == "__main__":
    unittest.main()

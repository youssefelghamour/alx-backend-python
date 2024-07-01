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

    @patch('client.get_json')
    @patch.object(GithubOrgClient, '_public_repos_url',
                  new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """ test public_repos function """
        # setup mocks

        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/google/repos"
        )
        # mock_get_json mocks the repos_payload function
        # that calls get_json with the _public_repos_url
        repos_payload = [{"name": "truth"}, {"name": "autoparse"}]
        mock_get_json.return_value = repos_payload

        # create an instance of GithubOrgClient
        test_client = GithubOrgClient("google")

        # call the method under test
        repos = test_client.public_repos()

        # extract repository names from repos_payload
        expected_repo_names = [repo['name'] for repo in repos_payload]

        # assert the mocked methods were called once
        mock_get_json.assert_called_once()
        mock_public_repos_url.assert_called_once()

        # assert the result matches the expected payload
        self.assertEqual(repos, expected_repo_names)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ tests has_licence function """
        # call the method under test
        result = GithubOrgClient.has_license(repo, license_key)

        # assert the result matches the expected value
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

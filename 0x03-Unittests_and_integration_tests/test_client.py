#!/usr/bin/env python3
""" Unittests for the functions in client module """
import unittest
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from unittest.mock import patch, Mock, PropertyMock, MagicMock
from fixtures import TEST_PAYLOAD


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


# structure of the TEST_PAYLOAD from fixtures.py
"""
TEST_PAYLOAD = [
    (
        {"repos_url": "https://api.github.com/orgs/google/repos"},  # org_data
        [
            {"name": "episodes.dart"},  # repos_data
            {"name": "cpp-netlib"}
        ]
    ),
]
"""
# The @parameterized_class decorator takes actual data from fixtures.py and
# assigns them to the attributes:
#       ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
# which are then passed to the TestIntegrationGithubOrgClient class as
# attributes or data sets for testing.


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ integration test for public_repos """

    @classmethod
    def setUpClass(cls):
        """ setup method """
        # Define a function to handle the behavior
        # of the mocked 'requests.get'
        def get_side_effect(url):
            # Define the URL that triggers returning org_payload
            test_url = "https://api.github.com/orgs/google"

            # If the requested URL matches test_url,
            if url == test_url:
                # returns a mock object with a json method that
                # that returns org_payload
                return MagicMock(json=lambda: cls.org_payload)
            # return repos_payload as a MagicMock with a
            # json method for any other URL
            return MagicMock(json=lambda: cls.repos_payload)

        # Patch 'requests.get' to replace it with a MagicMock for testing
        cls.get_patcher = patch('requests.get', side_effect=get_side_effect)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """ Test case for public_repos method """
        # create an instance of GithubOrgClient with mocked data
        client = GithubOrgClient("google")

        # assume public_repos fetches repositories based on org_payload
        repos = client.public_repos()

        # assert that the retrieved repositories match expected_repos
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """ tests public_repos with 'apache-2.0' license filter"""
        client = GithubOrgClient("google")
        repos = client.public_repos("apache-2.0")
        self.assertEqual(repos, self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """ stops the patcher """
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
""" Unittests for the functions in utils module """
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """ test cases for access_nested_map function """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ tests access_nested_map with different inputs """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """ tests KeyError with the above inputs """
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
        self.assertEqual(repr(e.exception), f"KeyError('{str(path[-1])}')")


class TestGetJson(unittest.TestCase):
    """ test cases for get_json function """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """ test get_json function """
        # Create a mock response object
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # call the function
        result = get_json(test_url)

        # assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """ test cases for memoize function """

    def test_memoize(self):
        """ test the memoize function """

        class TestClass:
            """ class for testing """

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # patch a_method to mock its behavior
        with patch.object(TestClass, 'a_method') as mock_a_method:
            # create an instance of TestClass
            obj = TestClass()

            # call a_property twice
            result1 = obj.a_property()
            result2 = obj.a_property()

            # assert that a_method was called only once
            mock_a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()

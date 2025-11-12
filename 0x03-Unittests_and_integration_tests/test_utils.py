#!/usr/bin/env python3
"""Unit tests for utils module"""
import unittest
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Tests access_nested_map function"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Tests access_nested_map function for exceptions
            and invalid key paths

            The test asserts that:
            - A KeyError is raised
            - The exception message equals the missing key that caused
                the error because we raise KeyError(key) (key is the message)
                in our test cases it's the last key: path[-1]
        """
        # Use assertRaises context manager to check for KeyError
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        # Verify the exception message (stored in exception.args[0])
        self.assertEqual(context.exception.args[0], path[-1])


class TestGetJson(unittest.TestCase):
    """Tests for get_json function"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Tests get_json function"""
        mock_get.return_value.json.return_value = test_payload

        # Call the function being tested
        result = get_json(test_url)

        # Assert that requests.get was called once with the test_url
        mock_get.assert_called_once_with(test_url)
        # Assert that the result matches the expected payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for memoize decorator"""

    def test_memoize(self):
        """Tests memoize decorator"""

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with patch.object(TestClass, 'a_method') as mock_a_method:
            # Set the return value for a_method
            mock_a_method.return_value = 42

            # Call the memoized method twice
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            # Assert that the results are the same
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            # Assert that a_method was called only once due to memoization
            mock_a_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()

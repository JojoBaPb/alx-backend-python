#!/usr/bin/env python3
"""
Unit test module for utils.py.
Covers Tasks 0 through 3.
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test class for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns correct values"""
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path, exception):
        """Test access_nested_map raises KeyError for invalid paths"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test class for get_json"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test get_json returns correct JSON data"""
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        with patch("requests.get", return_value=mock_response):
            result = get_json(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test class for memoize"""

    def test_memoize(self):
        """Test that memoize caches method output"""
        class TestClass:
            """Test class for memoization"""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

      with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()
            first = obj.a_property
            second = obj.a_property
            self.assertEqual(first, 42)
            self.assertEqual(second, 42)
            mock_method.assert_called_once()

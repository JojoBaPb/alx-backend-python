#!/usr/bin/env python3
"""
Unittest module for utils.py
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, memoize
from unittest.mock import patch
from typing import Mapping, Sequence, Any


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any):
        """Test that access_nested_map returns expected result"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence, expected_exception: Exception):
        """Test that access_nested_map raises KeyError on invalid path"""
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator"""

    def test_memoize(self):
        """Test memoization on a method"""

        class TestClass:
            """Simple test class"""
            def __init__(self):
                self.call_count = 0

            @memoize
            def a_method(self):
                """A method to be memoized"""
                self.call_count += 1
                return 42

        obj = TestClass()

        # Call the method twice and assert only one actual call was made
        self.assertEqual(obj.a_method(), 42)
        self.assertEqual(obj.a_method(), 42)
        self.assertEqual(obj.call_count, 1)


if __name__ == '__main__':
    unittest.main()


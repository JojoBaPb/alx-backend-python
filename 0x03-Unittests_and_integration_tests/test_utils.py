#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map"""
import unittest
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map"""

    def test_access_nested_map(self):
        """Test standard access"""
        self.assertEqual(access_nested_map({"a": 1}, ("a",)), 1)
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a",)), {"b": 2})
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a", "b")), 2)

    def test_access_nested_map_exception(self):
        """Test missing key raises KeyError"""
        with self.assertRaises(KeyError):
            access_nested_map({}, ("a",))
        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ("a", "b"))


if __name__ == "__main__":
    unittest.main()

